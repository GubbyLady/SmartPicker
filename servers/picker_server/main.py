#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:57
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : main
# @Software: PyCharm
import threading

from core.constant import CV_SERVER, PICKER_SERVER
from core.message_class import Message,create_message
from servers.picker_server.constant import PickerConstant
from core.tools import Loggers

class PickerMain:
    def __init__(self, send_queue, recv_queue):
        self.send_queue = send_queue
        self.recv_queue = recv_queue
        self.Init()

    def Init(self):
        Loggers()
        PickerConstant()
        threading.Thread(target=self.listen_recv_queue).start()

    def listen_recv_queue(self):
        # 对接收的队列进行监听
        while True:
            if self.recv_queue.qsize() != 0:
                # 接收队列不为空
                print(self.recv_queue.get())
            else:
                pass

    def send_message(self):
        message = create_message(send_server=PICKER_SERVER, recv_server=CV_SERVER,obj=None,op=None,value=None)
        self.send_queue.put(message)

if __name__ == '__main__':
    # print("picker服务启动")
    pass