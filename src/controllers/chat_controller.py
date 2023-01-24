from gi.overrides import GLib

import src.globals
from src.api.api import send_p2p_message, send_p2g_message, get_group_name, get_group_member_num, get_contact_list, \
    is_contact_group, get_nickname_by_id, get_p2p_messages_after_time, get_p2g_messages_after_time

from src.utils import get_cached_user_id, append_cached_group_list, is_id_in_group_cache, \
    append_to_cached_contact_list, get_cached_contact_list, get_cached_selected_contact_id, get_text_buffer_cache
from src.utils.common_utils import write_log
from src.utils.message_utils import *


def send_p2p_message_worker(receiver_id, content):
    send_p2p_message(receiver_id, content)


def send_group_message_worker(group_id, content):
    send_p2g_message(group_id, content)


def init_local_storage():
    contact_id_list = get_contact_list(get_cached_user_id())
    write_log("contact_list: " + str(contact_id_list))
    for contact_id in contact_id_list:
        is_group_id = is_contact_group(contact_id)
        if is_group_id:
            write_log("group_id: " + str(contact_id))
            append_cached_group_list(contact_id)
    for contact_id in contact_id_list:
        local_latest_message_time = get_local_latest_message_time(contact_id)
        if not is_id_in_group_cache(contact_id):
            p2p_messages_after_time = get_p2p_messages_after_time(contact_id, local_latest_message_time)
            for message in p2p_messages_after_time:
                append_message_storage(contact_id, False, message["content"], message["create_time"])
            latest_message = get_local_latest_message(contact_id)
            if latest_message is not None:
                local_latest_message_time = get_local_latest_message_time(contact_id)
            else:
                latest_message = {'message_content': "", 'is_sender': False, 'sent_time': int(round(time.time()*1000))}
                local_latest_message_time = latest_message['sent_time']
            nickname = get_nickname_by_id(contact_id)
            append_to_cached_contact_list(contact_id, nickname, latest_message['message_content'], local_latest_message_time)
        else:
            p2g_message_after_time = get_p2g_messages_after_time(contact_id, local_latest_message_time)
            for message in p2g_message_after_time:
                append_group_message_storage(contact_id, False, message["content"], message["create_time"], message["sender_name"])
            latest_message = get_local_latest_message(contact_id)
            if latest_message is not None:
                local_latest_message_time = get_local_latest_message_time(contact_id)
            else:
                latest_message = {'message_content': "", 'is_sender': False, 'sent_time': int(round(time.time()*1000))}
                local_latest_message_time = latest_message['sent_time']
            group_name = get_group_name(contact_id)
            append_to_cached_contact_list(contact_id, group_name, latest_message['message_content'], local_latest_message_time)
    write_log("拉取消息成功 return")


def init_chat_window(chat_window):
    write_log("开始初始化聊天窗口")
    """
    chat窗口的初始化工作
    1.读取cache里的联系人列表
    2.读取cache里的消息记录
    3.生成联系人ContactItem和对应聊天记录列表的映射关系
    4.将联系人列表和聊天记录列表添加到chat窗口的对应容器中
    """
    contact_list = get_cached_contact_list()
    """从本地cache中取出所有的本地联系人列表"""
    for contact in contact_list:
        is_selected = False
        contact_nickname = contact['nickname']
        contact_id = contact['contact_id']
        contact_sent_time = contact['sent_time']
        contact_last_message = contact['last_message']
        message_list = get_stored_messages(contact_id)

        """如果用户上一次使用过程中选中的是该联系人，则在打开chat窗口时，将该联系人的聊天记录列表显示出来，并将字体small化，以凸显选中"""
        if get_cached_selected_contact_id() == contact_id:
            is_selected = True
            """将本地消息记录列表填入聊天记录列表容器中"""
            if is_id_in_group_cache(contact_id):
                for message in message_list:
                    chat_window.insert_group_message(message['message_content'], message['is_sender'], message['sender_name'])
                group_name = get_group_name(contact_id)
                member_num = get_group_member_num(contact_id)
                chat_window.message_header_bar.set_title(group_name + " (" + str(member_num) + ")")
            else:
                for message in message_list:
                    chat_window.insert_message(message["message_content"], message["is_sender"])
                """将联系人昵称填入Header Bar里"""
                chat_window.message_header_bar.set_title(contact_nickname)

        """读入上次退出程序，text buffer中的内容"""
        text = get_text_buffer_cache(contact_id)
        chat_window.text_box.get_buffer().set_text(text)
        chat_window.insert_contact(contact_nickname, contact_last_message, contact_sent_time, contact_id, is_selected)
    write_log("拉取消息成功,show窗口")


def __insert_message_from_contact(chat_window, contact_id, sent_time, message_content):
    """
        本函数用于接收到消息后，将消息插入到聊天记录json中
        :param chat_window: Gtk.Window
        :param contact_id: 向当前用户发消息的联系人
        :param sent_time: 消息发送的时间戳,13位毫秒级UNIX时间戳
        :param message_content: 消息内容
    """
    append_message_storage(contact_id, False, message_content, sent_time)
    is_selected = False
    if src.globals.LAST_SELECTED_CONTACT.contact_id == contact_id:
        is_selected = True
        GLib.idle_add(chat_window.insert_message, message_content, False)
    GLib.idle_add(src.globals.LAST_SELECTED_CONTACT.update_contact, message_content, sent_time, is_selected)
    chat_window.scroll_flag = not chat_window.scroll_flag


def __insert_message_from_group(chat_window, group_id, sender_id, sender_name, sent_time, message_content):
    """
        本函数用于接收到消息后，将消息插入到聊天记录json中
        :param chat_window: Gtk.Window
        :param group_id: 向当前用户发消息的群组
        :param sender_id: 消息发送者
        :param sender_name: 消息发送者昵称
        :param sent_time: 消息发送的时间戳,13位毫秒级UNIX时间戳
        :param message_content: 消息内容
    """
    GLib.idle_add()
    print("insert message from group")
    append_group_message_storage(group_id, False, message_content, sent_time, sender_name)
    write_log("appended to cache")
    is_selected = False
    if src.globals.LAST_SELECTED_CONTACT.contact_id == group_id:
        is_selected = True
        GLib.idle_add(chat_window.insert_group_message, message_content, False, sender_name)
    GLib.idle_add(src.globals.LAST_SELECTED_CONTACT.update_contact, message_content, sent_time, is_selected)
    chat_window.scroll_flag = not chat_window.scroll_flag


def parse_p2p_msg_api_result(chat_window, msg_list):
    write_log("parse_p2p_msg_api_result"+str(msg_list))
    for message in msg_list:
        __insert_message_from_contact(chat_window,
                                      message["senderID"],
                                      message["create_time"],
                                      message["content"])


def parse_p2g_msg_api_result(chat_window, msg_list):
    write_log("parse_p2g_msg_api_result")
    write_log(str(isinstance(msg_list, list)))
    for message in msg_list:
        __insert_message_from_group(chat_window,
                                    message["groupID"],
                                    message["senderID"],
                                    message["sender_name"],
                                    message["create_time"],
                                    message["content"])
