import signal

from src.api.api import *
from gi.repository import Gtk
from datetime import time
import gi

import src.globals
from src.utils.common_utils import *
from src.utils.cache_utils import *
from .add_contact import AddContactWindow
from .create_group import CreateGroupWindow
from .join_group import JoinGroupWindow
from ..controllers.chat_controller import send_p2p_message_worker, send_group_message_worker
from ..globals.threading_pool import THREADING_POOL
gi.require_version("Gtk", "3.0")
global LAST_SELECTED_CONTACT
global CONTACT_MESSAGE_MAP


@Gtk.Template(filename="./glade_template/chat/chat.glade")
class ChatWindow(Gtk.Window):
    __gtype_name__ = "chat_window"
    provider = Gtk.CssProvider()
    provider.load_from_path('./glade_css/style.css')
    contact_list_box = Gtk.Template.Child("contact_listbox")
    message_list_box = Gtk.Template.Child("message_listbox")
    text_box = Gtk.Template.Child("text_box")
    message_header_bar = Gtk.Template.Child("message_header_bar")
    message_scroll_window = Gtk.Template.Child("message_scroll_window")
    scroll_flag = True

    def insert_contact(self, nickname, last_message, sent_time, contact_id, is_selected):
        write_log("insert_contact"+str(contact_id))
        write_log("insert_contact"+str(nickname))
        write_log("insert_contact"+str(last_message))
        sent_time = time.strftime("%m-%d %H:%M", time.localtime(sent_time/1000))
        if is_selected:
            nickname = add_small_label(nickname)
            last_message = add_small_label(last_message)
            sent_time = add_small_label(sent_time)
        contact_item = ContactItem(nickname, last_message, sent_time, contact_id)
        if is_selected:
            src.globals.LAST_SELECTED_CONTACT = contact_item
        self.contact_list_box.insert(contact_item, -1)
        self.contact_list_box.show_all()

    def insert_message(self, message, is_sender):
        message_item = MessageItem(message, is_sender)
        self.message_list_box.insert(message_item, -1)
        self.message_list_box.show_all()

    def insert_group_message(self, content, is_sender, sender_name):
        message_item = GroupMessageItem(sender_name, content, is_sender)
        self.message_list_box.insert(message_item, -1)
        self.message_list_box.show_all()

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        """保存输入区的内容，并退出程序"""
        write_log("退出程序")
        text_buffer = self.text_box.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), True)
        if src.globals.LAST_SELECTED_CONTACT is not None:
            set_text_buffer_cache(src.globals.LAST_SELECTED_CONTACT.contact_id, text)
        logout()
        os.kill(src.globals.PARENT_PID, signal.SIGUSR2)
        Gtk.main_quit()

    @Gtk.Template.Callback()
    def on_send_btn_clicked(self, *args):
        print("send")
        text_buffer = self.text_box.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), True)
        if text == "":
            return
        time_now = (lambda: int(time.time() * 1000))()
        src.globals.LAST_SELECTED_CONTACT.update_contact(text, time_now, True)
        text_buffer.set_text("")
        set_text_buffer_cache(get_cached_selected_contact_id(), "")
        print(src.globals.LAST_SELECTED_CONTACT)
        if is_id_in_group_cache(src.globals.LAST_SELECTED_CONTACT.contact_id):
            sender_name = get_cached_nickname()
            append_group_message_storage(src.globals.LAST_SELECTED_CONTACT.contact_id, True, text, time_now, sender_name)
            self.insert_group_message(text, True, get_cached_nickname())
            THREADING_POOL.submit(send_group_message_worker, src.globals.LAST_SELECTED_CONTACT.contact_id, text)
        else:
            append_message_storage(get_cached_selected_contact_id(), True, text, time_now)
            self.insert_message(text, True)
            self.scroll_flag = not self.scroll_flag
            THREADING_POOL.submit(send_p2p_message_worker, get_cached_selected_contact_id(), text)

    @Gtk.Template.Callback()
    def on_contact_row_selected(self, listbox, row, *args):
        self.scroll_flag = not self.scroll_flag
        if row is None:
            return
        if row == src.globals.LAST_SELECTED_CONTACT:
            return
        contact_id = row.contact_id
        text_buffer = self.text_box.get_buffer()
        last_contact_text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), True)
        set_text_buffer_cache(get_cached_selected_contact_id(), last_contact_text)
        text = get_text_buffer_cache(contact_id)
        self.text_box.get_buffer().set_text(text)
        if src.globals.LAST_SELECTED_CONTACT is not None:
            src.globals.LAST_SELECTED_CONTACT.restore_selected()
        set_cached_selected_contact_id(contact_id)
        src.globals.LAST_SELECTED_CONTACT = row
        row.set_selected()
        is_group = is_id_in_group_cache(contact_id)
        self.message_list_box.foreach(lambda x: self.message_list_box.remove(x))
        if is_group:
            group_name = get_group_name(contact_id)
            member_num = get_group_member_num(contact_id)
            self.message_header_bar.set_title(group_name + " (" + str(member_num) + ")")
            for message in get_stored_messages(contact_id):
                self.insert_group_message(message["message_content"], message["is_sender"], message["sender_name"])
        else:
            self.message_header_bar.set_title(row.get_nickname())
            for message in get_stored_messages(contact_id):
                new_message = MessageItem(message["message_content"], message["is_sender"])
                self.message_list_box.insert(new_message, -1)
        self.message_list_box.show_all()

    @Gtk.Template.Callback()
    def on_scroll_window_size_allocate(self, *args):
        if self.scroll_flag:
            self.scroll_flag = not self.scroll_flag
            adjustment = self.message_scroll_window.get_vadjustment()
            adjustment.set_value(adjustment.get_upper())

    @Gtk.Template.Callback()
    def on_add_contact_clicked(self, *args):
        add_contact_window = AddContactWindow()
        add_contact_window.show_all()

    @Gtk.Template.Callback()
    def on_create_group_clicked(self, *args):
        create_group_window = CreateGroupWindow()
        create_group_window.show_all()

    @Gtk.Template.Callback()
    def on_add_group_clicked(self, *args):
        add_group_window = JoinGroupWindow()
        add_group_window.show_all()


class ContactItem(Gtk.ListBoxRow):
    """
        该类继承自Gtk.ListBoxRow，代表一位联系人
        构造函数接受4个参数
        :param nickname: 昵称
        :param last_message: 最新消息的摘要
        :param sent_time: 本地存有的最新消息的发送时间，时间戳
        :param contact_id: 联系人的id
    """
    def __init__(self, nickname, last_message, sent_time, contact_id):
        super().__init__()
        self.contact_id = contact_id
        contact_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        sub_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        nickname_label = Gtk.Label(xalign=0)
        nickname_label.set_markup(nickname)
        last_message_label = Gtk.Label(xalign=0)
        last_message_label.set_markup(last_message)
        sub_box.pack_start(nickname_label, True, True, 0)
        sub_box.pack_start(last_message_label, True, True, 0)
        sent_time_label = Gtk.Label(xalign=1)
        sent_time_label.set_markup(sent_time)
        contact_box.pack_start(sub_box, True, True, 0)
        contact_box.pack_start(sent_time_label, False, False, 0)
        self.add(contact_box)

    def update_contact(self, last_message, sent_time, is_selected):
        nickname = self.get_nickname()
        update_cached_contact(self.contact_id, nickname, last_message, sent_time)
        if is_selected:
            nickname = add_small_label(self.get_nickname())
            last_message = add_small_label(last_message)
            sent_time = time.strftime("%m-%d %H:%M", time.localtime(sent_time/1000))
            sent_time = add_small_label(sent_time)
        self.get_child().get_children()[0].get_children()[0].set_markup(nickname)
        self.get_child().get_children()[0].get_children()[1].set_markup(last_message)
        self.get_child().get_children()[1].set_markup(sent_time)

    def restore_selected(self):
        contact_box = self.get_children()[0]
        children = contact_box.get_children()
        nickname_label = children[0].get_children()[0]
        last_message_label = children[0].get_children()[1]
        sent_time_label = children[1]
        nickname_label.set_markup(remove_small_label(nickname_label.get_text()))
        last_message_label.set_markup(remove_small_label(last_message_label.get_text()))
        sent_time_label.set_markup(remove_small_label(sent_time_label.get_text()))
        self.show_all()

    def set_selected(self):
        contact_box = self.get_children()[0]
        children = contact_box.get_children()
        nickname_label = children[0].get_children()[0]
        last_message_label = children[0].get_children()[1]
        sent_time_label = children[1]
        nickname_label.set_markup(add_small_label(nickname_label.get_text()))
        last_message_label.set_markup(add_small_label(last_message_label.get_text()))
        sent_time_label.set_markup(add_small_label(sent_time_label.get_text()))
        self.show_all()

    def get_nickname(self):
        contact_box = self.get_children()[0]
        children = contact_box.get_children()
        nickname_label = children[0].get_children()[0]
        return remove_small_label(nickname_label.get_text())


class MessageItem(Gtk.ListBoxRow):
    """
        该类继承自Gtk.ListBoxRow，代表一条消息
        该类的构造函数接收两个参数，分别是
        :param content: 消息内容
        :param is_sender: 用户自己是否是发送者
    """
    def __init__(self, content, is_sender):
        super().__init__()
        message_item_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        message_label = Gtk.Label(content)
        style_context = message_label.get_style_context()
        style_context.add_class("message-box")
        if is_sender:
            style_context.add_class("sent")
            message_item_box.pack_end(message_label, False, False, 0)
        else:
            message_item_box.pack_start(message_label, False, False, 0)
        self.add(message_item_box)


class GroupMessageItem(Gtk.ListBoxRow):
    """
        该类继承自Gtk.ListBoxRow，代表一条群消息
        该类的构造函数接收三个参数，分别是
        :param sender_name: 发送者昵称
        :param content: 消息内容
        :param is_sender: 用户自己是否是发送者
    """

    def __init__(self, sender_name, content, is_sender):
        super().__init__()
        message_item_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        message_label = Gtk.Label(content)
        style_context = message_label.get_style_context()
        style_context.add_class("message-box")
        if is_sender:
            style_context.add_class("sent")
            message_item_box.pack_end(message_label, False, False, 0)
            sender_label = Gtk.Label(sender_name)
            sender_label.set_markup(add_small_label(group_sender_name_font_wrapper(sender_name)))
            message_item_box.pack_start(sender_label, False, False, 0)
        else:
            message_item_box.pack_start(message_label, False, False, 0)
            sender_label = Gtk.Label(sender_name)
            sender_label.set_markup(add_small_label(group_sender_name_font_wrapper(sender_name)))
            message_item_box.pack_end(sender_label, False, False, 0)
        self.add(message_item_box)
