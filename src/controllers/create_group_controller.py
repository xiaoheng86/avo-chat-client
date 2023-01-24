import time

from gi.overrides import GLib

import src.globals
from src.api.api import create_group
from src.utils.cache_utils import *


def create_group_worker(gtk_spinner, group_name):
    """
        创建群聊
        :param group_name: 群聊名称
    """
    new_group_id = create_group(group_name)
    if new_group_id is not None:
        append_cached_group_list(new_group_id)
        now_time = int(round(time.time() * 1000))
        append_to_cached_contact_list(new_group_id, group_name, "", now_time)
        GLib.idle_add(src.globals.CHAT_WINDOW.insert_contact, group_name, "", now_time, new_group_id, False)
    gtk_spinner.stop()
