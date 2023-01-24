"""
    初始化线程池
    将监听管道FD是否有notify消息到来交由线程池处理
"""
from concurrent.futures import ThreadPoolExecutor

from src.globals.constants import MAX_WORKER

THREADING_POOL = ThreadPoolExecutor(max_workers=MAX_WORKER)
