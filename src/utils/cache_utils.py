from src.api.api import get_nickname_by_id
from src.utils.common_utils import write_log
from src.utils.message_utils import *

"""
    缓存信息
    cache_dict为全局变量，字典类型
    可保存userID和password等等
    当前被选中的contact ID
"""
CACHE_DICT = {}


def load_cache_from_file():
    global CACHE_DICT
    if os.path.exists("storage/cache.json"):
        with open("./storage/cache.json", "r", encoding="utf-8") as f:
            CACHE_DICT = json.load(f)


def append_cached_group_list(group_id):
    group_id = int(group_id)
    if "group_list" not in CACHE_DICT:
        CACHE_DICT["group_list"] = []
    if group_id not in CACHE_DICT["group_list"]:
        CACHE_DICT["group_list"].append(group_id)
    else:
        print("group id already in cache")


def is_id_in_group_cache(contact_id):
    if "group_list" not in CACHE_DICT:
        return False
    return contact_id in CACHE_DICT["group_list"]


def get_cached_nickname():
    if 'nickname' not in CACHE_DICT:
        CACHE_DICT['nickname'] = get_nickname_by_id(get_cached_user_id())
    return CACHE_DICT.get("nickname")


def set_cached_nickname(nickname):
    CACHE_DICT["nickname"] = nickname


def get_cached_user_id():
    if "userID" not in CACHE_DICT:
        return None
    return int(CACHE_DICT.get("userID"))


def set_cached_user_id(user_id):
    CACHE_DICT["userID"] = user_id


def set_cached_user_password(password):
    CACHE_DICT["password"] = password


def get_cached_user_password():
    if "password" not in CACHE_DICT:
        return None
    return CACHE_DICT.get("password")


def set_cached_selected_contact_id(user_id):
    user_id = int(user_id)
    CACHE_DICT["selected_contact_id"] = user_id


def get_cached_selected_contact_id():
    if 'selected_contact_id' not in CACHE_DICT:
        contact_list = get_cached_contact_list()
        if len(contact_list) > 0:
            contact_id = contact_list[0]["contact_id"]
            set_cached_selected_contact_id(contact_id)
    return CACHE_DICT['selected_contact_id']


def init_cached_contact_list():
    contact_list = CACHE_DICT["contact_list"]
    for contact in contact_list:
        contact_id = contact["contact_id"]
        get_local_latest_message(contact_id)


def append_to_cached_contact_list(contact_id, nickname, last_message, sent_time):
    if "contact_list" not in CACHE_DICT:
        CACHE_DICT["contact_list"] = []
    for contact_obj in CACHE_DICT["contact_list"]:
        if contact_obj["contact_id"] == contact_id:
            return
    CACHE_DICT["contact_list"].append({
        "contact_id": contact_id,
        "nickname": nickname,
        "last_message": last_message,
        "sent_time": sent_time
    })


def get_cached_contact_list():
    if "contact_list" not in CACHE_DICT:
        return []
    return CACHE_DICT['contact_list']


def remove_contact_in_cache(contact_id):
    if "contact_list" in CACHE_DICT:
        CACHE_DICT["contact_list"].remove(contact_id)


def update_cached_contact(contact_id, nickname, last_message, sent_time):
    if "contact_list" in CACHE_DICT:
        for contact in CACHE_DICT["contact_list"]:
            if contact["contact_id"] == contact_id:
                contact["nickname"] = nickname
                contact["last_message"] = last_message
                contact["sent_time"] = sent_time


def set_text_buffer_cache(contact_id, text):
    contact_id = str(contact_id)
    write_log("set_text_buffer_cache")
    if "text_buffer" not in CACHE_DICT:
        CACHE_DICT["text_buffer"] = {}
    CACHE_DICT["text_buffer"][contact_id] = text
    write_log("set text buffer cache"+str(CACHE_DICT))


def get_text_buffer_cache(contact_id):
    contact_id = str(contact_id)
    if "text_buffer" not in CACHE_DICT:
        return ""
    contact_text_buffer = CACHE_DICT["text_buffer"]
    if contact_id not in contact_text_buffer:
        return ""
    return CACHE_DICT['text_buffer'][contact_id]


@atexit.register
def write_cache_to_file():
    """注册为atexit函数，程序退出时自动调用"""
    print("write_cache_to_file")
    with open("./storage/cache.json", "w", encoding="utf-8") as f:
        json.dump(CACHE_DICT, f, ensure_ascii=False, indent=4)
