#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:58
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : servers_class
# @Software: PyCharm
"""
该文件书各个服务的类,并使用单例模式
"""
from core.tools import singleton
from servers.cv_server.main import CvMain
from servers.picker_server.main import PickerMain

@singleton
class CvServer():
    def __init__(self,send_queue,recv_queue):
        # print(f"CV:{send_queue}")
        CvMain(send_queue,recv_queue)

    def start(self):
        pass

@singleton
class PickerServer():
    def __init__(self,send_queue,recv_queue):
        PickerMain(send_queue,recv_queue)

    def start(self):
        pass


