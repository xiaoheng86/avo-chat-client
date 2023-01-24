import src.globals.constants
from src.globals import constants
from src.api.requests_wrapper import http_post, http_post_without_token, http_get
from src.exception.business_exception import BusinessException
from src.controllers.chat_controller import *
from src.utils.cache_utils import *
from src.utils.common_utils import write_log


def user_register(nickname, password):
    """用户注册"""
    payload = {
        "nickname": nickname,
        "password": password
    }
    """result是一个dict类型"""
    write_log("注册信息："+str(payload))
    result = http_post_without_token(constants.USER_REGISTER_URL, json=payload).json()
    if result["code"] == 200:
        return result["data"]["userID"]
    else:
        raise BusinessException("注册失败："+result["message"])


def user_login(user_id, password):
    """用户登录"""
    payload = {
        "userID": user_id,
        "password": password
    }
    """result是一个dict类型"""
    result = http_post_without_token(constants.USER_LOGIN_URL, json=payload).json()
    token = result["data"]["token"]
    if token is not None:
        from src.api.protocol import write_local_token
        write_local_token(token)
        src.globals.constants.TOKEN = token
        return True
    else:
        write_log("登录失败："+result["message"])
        raise BusinessException("登录失败："+result["message"])


def get_p2p_messages_after_time(sender_id, after_time):
    """拉取其他用户在after_time之后发给当前用户的消息"""
    payload = {
        "senderID": sender_id,
        "receiverID": int(get_cached_user_id()),
        "after_time": after_time
    }
    result = http_get(constants.P2P_MESSAGE_URL, json=payload).json()
    if result["code"] == 200:
        """result["data"]是一个list"""
        if "data" in result:
            return result["data"]
        else:
            write_log("无最新消息")
            return []
    else:
        write_log("拉取消息失败："+result["message"])
        raise BusinessException("拉取消息失败："+result["message"])


def get_nickname_by_id(user_id):
    user_id = int(user_id)
    """根据用户id获取用户昵称"""
    payload = {
        "userID": user_id
    }
    result = http_get(constants.USER_INFO_URL, json=payload).json()
    if result["code"] == 200:
        return result["data"]["nickname"]
    else:
        raise BusinessException("获取昵称失败："+result["message"])


def send_p2p_message(receiver_id, content):
    """发送点对点消息"""
    payload = {
        "senderID": get_cached_user_id(),
        "receiverID": int(receiver_id),
        "content": content
    }
    result = http_post(constants.P2P_MESSAGE_URL, json=payload).json()
    if result["code"] == 200:
        print("发送消息成功")
        return True
    else:
        raise BusinessException("发送消息失败："+result["message"])


def send_p2g_message(group_id, content):
    """发送群组消息"""
    payload = {
        "senderID": get_cached_user_id(),
        "groupID": int(group_id),
        "content": content
    }
    result = http_post(constants.P2G_MESSAGE_URL, json=payload).json()
    if result["code"] == 200:
        write_log("发送群组消息成功")
        return True
    else:
        raise BusinessException("发送消息失败："+result["message"])


def add_contact(user_id):
    """添加联系人"""
    payload = {
        "targetID": user_id,
        "operationType": constants.T_ADD_CONTACT
    }
    result = http_post(constants.USER_CONTACT_URL, json=payload).json()
    if result["code"] == 200:
        print("添加联系人成功")
        return True
    else:
        raise BusinessException("添加联系人失败："+result["message"])


def delete_contact(user_id):
    """删除联系人"""
    payload = {
        "targetID": user_id,
        "operationType": constants.T_DELETE_CONTACT
    }
    result = http_post(constants.USER_CONTACT_URL, json=payload).json()
    if result["code"] == 200:
        print("删除联系人成功")
        return True
    else:
        raise BusinessException("删除联系人失败："+result["message"])


def get_contact_list(user_id):
    """获取联系人列表"""
    user_id = int(user_id)
    payload = {
        "userID": user_id
    }
    result = http_get(constants.USER_CONTACT_URL, json=payload).json()
    if result["code"] == 200:
        """返回值是一个list"""
        return result["data"]["contact"]
    else:
        return []


def create_group(group_name):
    """创建群组"""
    payload = {
        "groupName": group_name
    }
    result = http_post(constants.GROUP_CREATE_URL, json=payload).json()
    if result["code"] == 200:
        print("创建群组成功")
        """result["data"]是一个list列表类型"""
        return result["data"]
    else:
        raise BusinessException("创建群组失败："+result["message"])


def get_group_member_num(group_id):
    group_id = int(group_id)
    """获取群组成员数量"""
    payload = {
        "groupID": group_id
    }
    result = http_get(constants.GROUP_INFO_URL, json=payload).json()
    if result["code"] == 200:
        return len(result["data"]["members"])
    else:
        raise BusinessException("获取群组成员数量失败："+result["message"])


def get_group_name(group_id):
    group_id = int(group_id)
    """获取群组名称"""
    payload = {
        "groupID": group_id
    }
    result = http_get(constants.GROUP_INFO_URL, json=payload).json()
    if result["code"] == 200:
        return result["data"]["groupName"]
    else:
        raise BusinessException("获取群组名称失败："+result["message"])


def get_p2g_messages_after_time(group_id, after_time):
    group_id = int(group_id)
    after_time = int(after_time)
    """拉取群组消息"""
    payload = {
        "groupID": group_id,
        "after_time": after_time
    }
    write_log("拉取群组消息，group_id="+str(group_id)+", after_time="+str(after_time))
    result = http_get(constants.P2G_MESSAGE_URL, json=payload).json()
    if result["code"] == 200:
        if "data" in result:
            write_log("p2g消息："+str(result["data"]))
            return result["data"]
        else:
            write_log("p2g消息：无最新消息")
            return []
    else:
        raise BusinessException("拉取群组消息失败："+result["message"])


def join_group(group_id):
    """加入群组"""
    payload = {
        "groupID": group_id
    }
    result = http_post(constants.GROUP_JOIN_URL, json=payload).json()
    if result["code"] == 200:
        print("加入群组成功")
        return True
    else:
        raise BusinessException("加入群组失败："+result["message"])


def get_group_name_by_id(group_id):
    group_id = int(group_id)
    """根据群组ID获取群组名称"""
    payload = {
        "groupID": group_id
    }
    result = http_get(constants.GROUP_INFO_URL, json=payload).json()
    if result["code"] == 200:
        return result["data"]["groupName"]
    else:
        raise BusinessException("根据群组ID获取群组名称失败："+result["message"])


def is_contact_group(contact_id):
    """判断id是否是群组id"""
    contact_id = int(contact_id)
    payload = {
        "targetID": contact_id
    }
    result = http_get(constants.IS_GROUP_URL, json=payload).json()
    if result["code"] == 200:
        return result["data"]["judgeRes"]
    else:
        raise BusinessException("判断id是否是群组id失败："+result["message"])


def logout():
    """退出登录"""
    write_log("退出登录")
    result = http_post(constants.USER_LOGOUT_URL).json()
    if result["code"] == 200:
        write_log("退出登录成功")
        return True
    else:
        raise BusinessException("退出登录失败："+result["message"])
