#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:57
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : main
# @Software: PyCharm
import threading
import time

import servers.constant
from servers.cv_server.constant import CvConstant
from core.tools import Logger
from core.constant import CV_SERVER,PICKER_SERVER,LOGGER_LEVEL
from core.message_class import create_message
from servers.constant import SERVER_LOG
# from core.log_handle import MyLog

class CvMain:
    def __init__(self,send_queue,recv_queue):
        servers.constant.SERVER_LOG = Logger(name="CV",level=LOGGER_LEVEL)
        self.log_handle = servers.constant.SERVER_LOG()
        self.send_queue = send_queue
        self.recv_queue = recv_queue
        self.Init()
        self.send_message() # TODO 测试一下
    def Init(self):
        CvConstant()
        threading.Thread(target=self.listen_recv_queue).start()

        # time.sleep(10)
        # self.send_message()

    def listen_recv_queue(self):
        # 对接收的队列进行监听
        while True:
            if self.recv_queue.qsize() != 0:
                # 接收队列不为空
                self.log_handle.info(self.recv_queue.get())
            else:
                pass

    def send_message(self):
        message = create_message(send_server=CV_SERVER,recv_server=PICKER_SERVER,obj="a",op="b",value="c")
        self.send_queue.put(message)
        self.log_handle.info(f"CV -- 已发送:f{message}")

if __name__ == '__main__':
    pass