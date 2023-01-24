#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2022 rainbow <rainbow@kali>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import gi
from gi.overrides.Gtk import Gtk

import src.globals
from src.utils.common_utils import write_log

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from src.exception.business_exception import BusinessException
from src.wins.login import LoginWindow

try:
    import sys
    from src.globals import PID, PIPE_FD
    from concurrent.futures import ThreadPoolExecutor
    from src.globals import *
    """
        导入自定义模块utils, __init__会自动初始化CACHE_DICT与MESSAGE_STORAGE_DICT
        后续所有对CACHE_DICT与MESSAGE_STORAGE_DICT的操作都是对这两个全局变量的操作
        注册了atexit函数，程序退出时自动调用，会将这两个全局字典变量写入json文件保存
    """
    from src.utils.cache_utils import *
    from src.utils.message_utils import *

    """
        通过当前进程ID和管道读端文件描述符FD值拼接出管道读端文件路径，将后续对管道的IO直接转换为文件IO
    """
    src.globals.PIPE_INPUT_PATH = os.path.join("/proc", str(PID), "fd", str(PIPE_FD))
    """
        加载CSS文件
    """
    screen = Gdk.Screen.get_default()
    provider = Gtk.CssProvider()
    provider.load_from_path("./glade_css/style.css")
    Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    """
        加载登录页的UI glade文件
    """
    log_window = LoginWindow()
    hd = log_window.get_titlebar()
    hd.get_style_context().add_provider(log_window.provider, 600)
    log_window.show()

    Gtk.main()
    exit(0)

except Exception as e:
    write_log(str(e))
    exit(-1)
