import datetime
import time


def check_nickname_length(nickname):
    """检查昵称长度"""
    if len(nickname) < 1 or len(nickname) > 20:
        return False
    return True


def check_password_length(password):
    """检查密码长度"""
    if len(password) < 6 or len(password) > 20:
        return False
    return True


def check_user_id_length(user_id):
    """检查用户ID长度"""
    if len(user_id) != 8:
        return False
    return True


def truncate_message(message: str, truncation: int = 4) -> str:
    """信息摘要，truncation为number数据类型的截断位数"""
    return message[:truncation]


def timestamp_to_string(timestamp: 'timestamp by Unix' = time.time()) -> str:
    """该函数将Unix时间戳转化为‘hh:mm’格式的字符串并返回"""
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime("%H:%M")


def add_small_label(content) -> str:
    """该函数将content添加小标签并返回"""
    return f'<small>{content}</small>'


def remove_small_label(content) -> str:
    """该函数将content移除小标签并返回"""
    return content.replace('<small>', '').replace('</small>', '')


def write_log(content):
    """该函数将content写入日志文件"""
    with open('/home/xiaoheng/Desktop/test/avo_c_gtk.log', 'a', encoding='utf-8') as f:
        f.write(content+'\n')


def group_sender_name_font_wrapper(sender_name) -> str:
    """该函数将sender_name添加标签并返回"""
    return f'<span foreground="grey" size="small"><i>{sender_name}</i></span>'
