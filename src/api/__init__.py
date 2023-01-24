"""
    @Author: https://github.com/xiaoheng86
    这个包负责HTTP API请求的封装
    api.py提供了本项目用到的所有HTTP请求
    protocol.py封装了由Linux管道传入的自定义的avo-protocol解析
    requests_wrapper.py封装了requests库的get和post方法，提供了带token和不带token的两种请求方式
"""
from .api import *
from .protocol import *
from .requests_wrapper import *
