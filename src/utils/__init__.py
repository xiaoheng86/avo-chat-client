"""
    @Author: https://github.com/xiaoheng86
    这个包提供了utils函数
    cache_utils.py提供了对全局缓存的操作，如remember me功能
    message_utils.py提供了对客户端本地消息记录的保存和读取的操作
    common_utils.py提供了一些常用的工具函数
"""

from .common_utils import *
from .cache_utils import *
from .message_utils import *
from .cache_utils import CACHE_DICT
"""
    在导入包的时候，会自动执行如下代码，将json文件中的信息读取到两个全局字典变量中
    程序执行过程中所有对json的操作都是对这两个字典的操作
    程序退出时，注册了atexit函数会自动将这两个字典写入json文件
"""
load_cache_from_file()
load_message_storage_json()
