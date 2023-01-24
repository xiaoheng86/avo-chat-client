import time

from gi.overrides import GLib

from src.api.api import join_group, get_group_name_by_id
from src.globals import CHAT_WINDOW
from src.utils.cache_utils import append_cached_group_list, append_to_cached_contact_list


def search_group_worker(gtk_spinner, gtk_label, group_id):
    """
        搜索群聊，并负责请求完成后关闭spinner,将nickname显示到label中
        :param group_id: 群聊ID
    """
    group_name = get_group_name_by_id(int(group_id))
    gtk_spinner.stop()
    gtk_label.set_text(str(group_name))
    print("got group_name %s, returning" % group_name)
    return group_name


def join_group_worker(gtk_window, gtk_spinner, gtk_message_label, group_id, group_name):
    """
        加入群聊
        :param group_id: 群聊ID
    """
    result = join_group(int(group_id))
    if result is True:
        gtk_message_label.set_text("加入群聊成功")
        append_cached_group_list(group_id)
        now_time = int(round(time.time() * 1000))
        append_to_cached_contact_list(group_id, group_name, "", now_time)
        GLib.idle_add(CHAT_WINDOW.insert_contact, group_name, "", now_time, group_id, False)
    gtk_spinner.stop()
    gtk_window.close()
