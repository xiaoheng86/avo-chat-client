import atexit
import json
import os
import time

from src.utils.common_utils import write_log

MESSAGE_STORAGE_DICT = {}

"""
    将客户端本地消息存入json文件
    文件结构为树形结构，每个节点对应一个联系人
    每个联系人里面存储的是一个列表，列表里面存储的是消息
    每个消息是一个字典，字典里面存储的是消息的内容
    每个消息的内容包括：
        "is_sender": 客户端是否为消息发送者(boolean)，
        "message_content": 消息的内容(text)，
        "message_time": 消息的发送时间(timestamp)
"""


def load_message_storage_json():
    global MESSAGE_STORAGE_DICT
    if os.path.exists("storage/message_storage.json"):
        with open("storage/message_storage.json", "r", encoding="utf-8") as f:
            MESSAGE_STORAGE_DICT = json.load(f)


def append_message_storage(contact_user_id, is_sender, message_content, message_time):
    contact_user_id = str(contact_user_id)
    """向本地消息存储中添加一条消息"""
    if contact_user_id not in MESSAGE_STORAGE_DICT:
        MESSAGE_STORAGE_DICT[contact_user_id] = []
    MESSAGE_STORAGE_DICT[contact_user_id].append({
        "is_sender": is_sender,
        "message_content": message_content,
        "message_time": message_time
    })
    write_log("append message storage MESSAGE_STORAGE_DICT is"+str(MESSAGE_STORAGE_DICT))


def append_group_message_storage(group_id, is_sender, message_content, message_time, sender_name):
    group_id = str(group_id)
    """向本地消息存储中添加一条消息"""
    if group_id not in MESSAGE_STORAGE_DICT:
        MESSAGE_STORAGE_DICT[group_id] = []
    MESSAGE_STORAGE_DICT[group_id].append({
        "is_sender": is_sender,
        "message_content": message_content,
        "message_time": message_time,
        "sender_name": sender_name
    })


@atexit.register
def write_message_storage_to_file():
    """注册为atexit函数，程序退出时自动调用"""
    print("write_message_storage_to_file")
    with open("storage/message_storage.json", "w", encoding="utf-8") as f:
        json.dump(MESSAGE_STORAGE_DICT, f, ensure_ascii=False, indent=4)


def get_local_latest_message_time(contact_user_id):
    """
        返回-1则表示没有消息
    """
    contact_user_id = str(contact_user_id)
    if contact_user_id not in MESSAGE_STORAGE_DICT:
        return -1
    messages = MESSAGE_STORAGE_DICT[contact_user_id]
    if len(messages) == 0:
        return -1
    messages.sort(key=lambda x: x["message_time"])
    return messages[-1]["message_time"]


def get_local_latest_message(contact_user_id):
    contact_user_id = str(contact_user_id)
    if contact_user_id not in MESSAGE_STORAGE_DICT:
        return None
    messages = MESSAGE_STORAGE_DICT[contact_user_id]
    if len(messages) == 0:
        return None
    messages.sort(key=lambda x: x["message_time"])
    return messages[-1]


def get_stored_messages(contact_user_id):
    write_log("MESSAGE_STORAGE_DICT is"+str(MESSAGE_STORAGE_DICT))
    """返回一个列表，列表里面存储的是消息"""
    contact_user_id = str(contact_user_id)
    if contact_user_id not in MESSAGE_STORAGE_DICT:
        return []
    return MESSAGE_STORAGE_DICT[contact_user_id]
