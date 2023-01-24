import time

from gi.repository import Gtk

from src.controllers.add_contact_controller import search_user_worker, add_contact_worker
from src.globals.threading_pool import THREADING_POOL
from src.utils.cache_utils import append_to_cached_contact_list
from src.utils.common_utils import write_log


@Gtk.Template(filename="./glade_template/plus_menu/add_contact.glade")
class AddContactWindow(Gtk.Window):
    __gtype_name__ = "add_contact_window"
    ety_userid = Gtk.Template.Child("ety_userid")
    ety_hint_label = Gtk.Template.Child("ety_hint_label")
    btn_add = Gtk.Template.Child("btn_add")
    new_id_label = Gtk.Template.Child("new_id_label")
    nickname_label = Gtk.Template.Child("nickname_label")
    spinner = Gtk.Template.Child("spinner")
    future_if_user_exist = None

    @staticmethod
    def __ety_error_hint(gtk_ety, gtk_label, message):
        gtk_ety.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, 'dialog-warning-symbolic')
        gtk_ety.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, 'Please check your input format')
        gtk_label.set_text(message)
        gtk_label.set_visible(True)

    @staticmethod
    def __ety_error_restore(gtk_ety, gtk_label):
        gtk_ety.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)
        gtk_ety.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, None)
        gtk_label.set_visible(False)

    @Gtk.Template.Callback()
    def on_text_changed(self, *args):
        ety_buffer = self.ety_userid.get_text()
        if len(ety_buffer) != 8 or not ety_buffer.isnumeric():
            self.__ety_error_hint(self.ety_userid, self.ety_hint_label, "User ID必须为8位数字")
        else:
            self.__ety_error_restore(self.ety_userid, self.ety_hint_label)
            self.spinner.start()
            self.future_if_user_exist = THREADING_POOL.submit(search_user_worker, self.spinner, self.nickname_label, ety_buffer)

    @Gtk.Template.Callback()
    def on_btn_add_clicked(self, *args):
        print("on_btn_add_clicked")
        nickname = None
        contact_id = None
        if self.future_if_user_exist is not None:
            nickname = self.future_if_user_exist.result()
            contact_id = int(self.ety_userid.get_text())
        if nickname is not None:
            self.spinner.start()
            self.btn_add.set_sensitive(False)
            self.ety_userid.set_sensitive(False)
            THREADING_POOL.submit(add_contact_worker, self, self.spinner, self.new_id_label, contact_id)
        else:
            self.new_id_label = "请检查输入的Contact ID是否正确\n或等待搜索完成"

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        write_log("add content destroy")
