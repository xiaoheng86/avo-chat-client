import src.globals.constants
from src.controllers.chat_controller import parse_p2p_msg_api_result, parse_p2g_msg_api_result
from src.globals.constants import T_P2P, T_P2G
from .api import get_p2p_messages_after_time, get_p2g_messages_after_time
from src.utils.common_utils import write_log
from src.utils.message_utils import *


def __read_a_json_from_pipe(pipe):
    """从管道中读取一个json，供pipe_listener函数调用"""
    json_size = int(pipe.read(4))
    if json_size == 0:
        return None
    json_str = pipe.read(json_size)
    print(json_str)
    return json.loads(json_str)


def pipe_listener(chat_window, pipe_output_path):
    write_log("pipe listening from " + pipe_output_path)
    with open(pipe_output_path, "r") as pipe:
        while True:
            notify = __read_a_json_from_pipe(pipe)
            write_log("pipe listener got a notify: " + str(notify))
            if notify is None:
                print("pipe closed")
                break
            if notify["type"] == T_P2P:
                print("p2p notify coming")
                handle_p2p_notify(chat_window, notify)
            elif notify["type"] == T_P2G:
                print("p2g notify coming")
                handle_p2g_notify(chat_window, notify)


def handle_p2p_notify(chat_window, notify_item):
    """
        处理通知
        向服务器主动拉取新消息
    """
    pull_target = notify_item["pull_target"]
    after_time = get_local_latest_message_time(pull_target)
    write_log("pulling messages after " + str(after_time))
    write_log("pulling messages from " + str(pull_target))
    response_result = get_p2p_messages_after_time(pull_target, after_time)
    write_log("pulling messages result: " + str(response_result))
    parse_p2p_msg_api_result(chat_window, response_result)


def handle_p2g_notify(chat_window, notify_item):
    """
        处理群聊通知
        向服务器主动拉取新消息
    """
    group_id = notify_item["pull_target"]
    after_time = get_local_latest_message_time(group_id)
    write_log("pulling messages after " + str(after_time))
    write_log("pulling messages from group: " + str(group_id))
    response_result = get_p2g_messages_after_time(group_id, after_time)
    write_log("pulled messages result: " + str(response_result))
    parse_p2g_msg_api_result(chat_window, response_result)


def load_local_token():
    """读本地保存的TOKEN文件"""
    with open("storage/token.txt", "r") as f:
        return f.read()


def write_local_token(token):
    """将全局变量TOKEN写入本地文件"""
    with open("storage/token.txt", "w") as f:
        f.write(token)
