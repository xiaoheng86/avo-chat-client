import time

from gi.repository import Gtk

from src.controllers.create_group_controller import create_group_worker
from src.controllers.join_group_controller import join_group_worker, search_group_worker
from src.globals.threading_pool import THREADING_POOL
from src.utils.cache_utils import append_to_cached_contact_list


@Gtk.Template(filename="./glade_template/plus_menu/join_group.glade")
class JoinGroupWindow(Gtk.Window):
    __gtype_name__ = "join_group_window"
    ety_group_id = Gtk.Template.Child("ety_group_id")
    group_name_label = Gtk.Template.Child("group_name_label")
    spinner = Gtk.Template.Child("spinner")
    btn_join = Gtk.Template.Child("btn_join")
    ety_hint_label = Gtk.Template.Child("ety_hint_label")
    message_label = Gtk.Template.Child("message_label")
    future_if_group_exist = None

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
        ety_buffer = self.ety_group_id.get_text()
        if len(ety_buffer) != 8 or not ety_buffer.isnumeric():
            self.__ety_error_hint(self.ety_group_id, self.ety_hint_label, "Group ID必须为8位数字")
        else:
            self.__ety_error_restore(self.ety_group_id, self.ety_hint_label)
            self.spinner.start()
            self.future_if_group_exist = THREADING_POOL.submit(search_group_worker, self.spinner, self.group_name_label, int(ety_buffer))

    @Gtk.Template.Callback()
    def on_btn_join_clicked(self, *args):
        print("on_btn_add_clicked")
        group_name = None
        group_id = int(self.ety_group_id.get_text())
        if self.future_if_group_exist is not None:
            group_name = self.future_if_group_exist.result()
        if group_name is not None:
            self.spinner.start()
            self.btn_join.set_sensitive(False)
            self.ety_group_id.set_sensitive(False)
            THREADING_POOL.submit(join_group_worker, self, self.spinner, self.message_label, group_id, group_name)
        else:
            self.message_label = "请检查输入的Contact ID是否正确\n或等待搜索完成"

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        print("on_destroy")
        self.close()
