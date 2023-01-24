import time

from gi.repository import Gtk

from src.controllers.add_contact_controller import search_user_worker, add_contact_worker
from src.controllers.create_group_controller import create_group_worker
from src.globals.threading_pool import THREADING_POOL
from src.utils.cache_utils import append_to_cached_contact_list


@Gtk.Template(filename="./glade_template/plus_menu/create_group.glade")
class CreateGroupWindow(Gtk.Window):
    __gtype_name__ = "create_group_window"
    ety_group_name = Gtk.Template.Child("ety_group_name")
    spinner = Gtk.Template.Child("spinner")
    ety_hint_label = Gtk.Template.Child("ety_hint_label")

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
        ety_buffer = self.ety_group_name.get_text()
        if len(ety_buffer) < 1 or len(ety_buffer) > 20:
            self.__ety_error_hint(self.ety_group_name, self.ety_hint_label, "群聊名称必须为1-20位字符")
        else:
            self.__ety_error_restore(self.ety_group_name, self.ety_hint_label)

    @Gtk.Template.Callback()
    def on_btn_create_clicked(self, *args):
        group_name = self.ety_group_name.get_text()
        if len(group_name) < 1 or len(group_name) > 20:
            self.__ety_error_hint(self.ety_group_name, self.ety_hint_label, "群聊名称必须为1-20位字符")
            return
        self.spinner.start()
        THREADING_POOL.submit(create_group_worker, self.spinner, group_name)

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        print("on_destroy")
        self.close()
