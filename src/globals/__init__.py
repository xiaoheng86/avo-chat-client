"""
    @Author: https://github.com/xiaoheng86
    这个包提供了项目中可能用到的全局变量
    constants.py中包含了各种URL的常量
    threading_pool.py中包含了供全局使用的线程池
"""
import os
import sys

from . import constants
from . import threading_pool

"""
   命令行启动参数示例: python3 {path_to_main.py} {python进程的pid} {管道读端文件描述符FD值}
   从命令行参数里提取出当前进程ID和管道读端文件描述符FD值
"""
argv = sys.argv
PARENT_PID = int(argv[1])
PID = os.getpid()
PIPE_FD = int(argv[2])
LAST_SELECTED_CONTACT = None
PIPE_INPUT_PATH = None
CHAT_WINDOW = None
