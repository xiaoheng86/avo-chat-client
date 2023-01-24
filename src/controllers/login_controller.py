import os
import signal

import src.globals
from src.api.api import user_login, get_nickname_by_id, user_register
from src.utils.cache_utils import set_cached_user_id, set_cached_user_password
from src.utils.common_utils import write_log

new_user_hints_template = """\
注册成功，欢迎使用avo-chat!
     您的user ID为：%d"""

login_hints_template = """\
登录成功，欢迎回来，%s"""


def register_worker(gtk_new_id_label, nickname, password, gtk_spinner, gtk_check_btn):
    new_user_id = user_register(nickname, password)
    write_log("注册成功，新用户ID为：" + str(new_user_id))
    is_mem_checked = gtk_check_btn.get_active()
    if is_mem_checked:
        set_cached_user_id(new_user_id)
        set_cached_user_password(password)
    gtk_spinner.stop()
    gtk_spinner.set_visible(False)
    hints = new_user_hints_template % new_user_id
    gtk_new_id_label.set_text(hints)
    gtk_new_id_label.set_visible(True)


def login_worker(gtk_login_window, gtk_spinner, gtk_check_btn, user_id, password):
    is_login_success = user_login(user_id, password)
    is_mem_checked = gtk_check_btn.get_active()
    if is_login_success and is_mem_checked:
        set_cached_user_id(user_id)
        set_cached_user_password(password)
        nickname = get_nickname_by_id(user_id)
        write_log("登录成功 " + nickname)
        gtk_login_window.new_id_label.set_text(login_hints_template % nickname)
    gtk_spinner.stop()
    gtk_spinner.set_visible(False)
    """登录成功后，通知父进程通信协议连接到服务器，然后关闭登录窗口"""
    os.kill(src.globals.PARENT_PID, signal.SIGUSR1)
    gtk_login_window.login_success_flag = True
    gtk_login_window.close()
