import gi

import src.globals
from src.controllers.chat_controller import init_chat_window, init_local_storage
from src.api.protocol import pipe_listener
from ..controllers.login_controller import login_worker, register_worker
from ..globals.threading_pool import THREADING_POOL
from ..utils.cache_utils import *
from ..utils.common_utils import write_log

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from src.wins.chat import ChatWindow


@Gtk.Template(filename="./glade_template/login/login.glade")
class LoginWindow(Gtk.Window):
    __gtype_name__ = "login_window"
    provider = Gtk.CssProvider()
    provider.load_from_path('./glade_css/style.css')
    check_mem = Gtk.Template.Child("check_mem")
    btn_submit = Gtk.Template.Child("btn_submit")
    ety_userid = Gtk.Template.Child("ety_userid")
    ety_password = Gtk.Template.Child("ety_password")
    hint_label1 = Gtk.Template.Child("hint_label1")
    hint_label2 = Gtk.Template.Child("hint_label2")
    new_id_label = Gtk.Template.Child("new_id_label")
    spinner = Gtk.Template.Child("spinner")
    toggle_flag = 0
    login_success_flag = False

    @staticmethod
    def __ety_error_hint(gtk_ety, gtk_label, message):
        gtk_ety.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, 'dialog-warning-symbolic')
        gtk_ety.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, '请检查输入')
        gtk_label.set_text(message)
        gtk_label.set_visible(True)

    @staticmethod
    def __ety_error_restore(gtk_ety, gtk_label):
        gtk_ety.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)
        gtk_ety.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, None)
        gtk_label.set_visible(False)

    @Gtk.Template.Callback()
    def onDestroy(self, *args):
        if not self.login_success_flag:
            write_log("login failed")
            Gtk.main_quit()
            return
        chat_window = ChatWindow()
        title_bar = chat_window.get_titlebar()
        title_bar.get_style_context().add_provider(chat_window.provider, 600)
        init_local_storage()
        init_chat_window(chat_window)
        chat_window.show_all()
        src.globals.CHAT_WINDOW = chat_window
        THREADING_POOL.submit(pipe_listener, chat_window, src.globals.PIPE_INPUT_PATH)

    @Gtk.Template.Callback()
    def onLoginToggled(self, *args):
        self.toggle_flag = (self.toggle_flag + 1) % 2
        self.new_id_label.set_text("")
        if self.toggle_flag == 1:
            cached_user_id = get_cached_user_id()
            cached_user_password = get_cached_user_password()
            if cached_user_id is None:
                self.ety_userid.set_text("")
            else:
                self.ety_userid.set_text(str(cached_user_id))
            if cached_user_password is None:
                self.ety_password.set_text("")
            else:
                self.ety_password.set_text(cached_user_password)
            self.ety_userid.set_placeholder_text("User ID")
            self.ety_userid.set_max_length(8)
        else:
            self.ety_userid.set_text("")
            self.ety_userid.set_placeholder_text("昵称")
            self.ety_userid.set_max_length(20)
            self.ety_password.set_text("")

    @Gtk.Template.Callback()
    def on_ety_userid_changed(self, *args):
        ety1_buffer = self.ety_userid.get_text()
        if self.toggle_flag == 1:
            if len(ety1_buffer) != 8 or not ety1_buffer.isnumeric():
                self.__ety_error_hint(self.ety_userid, self.hint_label1, "User ID必须为8位数字")
            else:
                self.__ety_error_restore(self.ety_userid, self.hint_label1)
        else:
            if len(ety1_buffer) < 1 or len(ety1_buffer) > 20:
                self.__ety_error_hint(self.ety_userid, self.hint_label1, "昵称长度必须在1-20之间")
            else:
                self.__ety_error_restore(self.ety_userid, self.hint_label1)

    @Gtk.Template.Callback()
    def on_ety_password_changed(self, *args):
        ety2_buffer = self.ety_password.get_text()
        if len(ety2_buffer) < 6 or len(ety2_buffer) > 20:
            self.__ety_error_hint(self.ety_password, self.hint_label2, "密码长度必须在6-20之间")
        else:
            self.__ety_error_restore(self.ety_password, self.hint_label2)

    @Gtk.Template.Callback()
    def onSubmit(self, *args):
        if self.hint_label1.get_visible() is False and self.hint_label2.get_visible() is False and self.ety_userid.get_text() != "" and self.ety_password.get_text() != "":
            if self.toggle_flag == 0:
                self.spinner.start()
                self.spinner.set_visible(True)
                THREADING_POOL.submit(register_worker, self.new_id_label, self.ety_userid.get_text(), self.ety_password.get_text(), self.spinner, self.check_mem)
            else:
                self.spinner.start()
                self.spinner.set_visible(True)
                THREADING_POOL.submit(login_worker, self, self.spinner, self.check_mem, self.ety_userid.get_text(), self.ety_password.get_text())

        else:
            self.new_id_label.set_text("请根据提示检查输入")
            self.new_id_label.set_visible(True)
