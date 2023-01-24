import time

from gi.overrides import GLib

import src.globals
from src.api.api import get_nickname_by_id, add_contact
from src.utils.cache_utils import append_to_cached_contact_list
from src.utils.common_utils import write_log


def search_user_worker(gtk_spinner, gtk_label, user_id):
    """
        搜索联系人，并负责请求完成后关闭spinner,将nickname显示到label中
        :param user_id: 联系人的user_id
    """
    nickname = get_nickname_by_id(int(user_id))
    gtk_spinner.stop()
    gtk_label.set_text(str(nickname))
    print("got nickname %s, returning" % nickname)
    return nickname


def add_contact_worker(gtk_window, gtk_spinner, gtk_label, user_id):
    """
        添加联系人
        :param user_id: 联系人的user_id
    """
    nickname = gtk_window.future_if_user_exist.result()
    write_log("add_contact_worker: nickname is %s" % nickname)
    contact_id = int(gtk_window.ety_userid.get_text())
    add_contact(int(user_id))
    write_log("add_contact_worker: add contact %s success nickname %s" % (contact_id, nickname))
    gtk_spinner.stop()
    gtk_label.set_text("添加成功")
    now_time = int(round(time.time() * 1000))
    append_to_cached_contact_list(contact_id, nickname, "", now_time)
    GLib.idle_add(src.globals.CHAT_WINDOW.insert_contact, nickname, "", now_time, contact_id, False)
    write_log("inserted")
    gtk_window.close()
