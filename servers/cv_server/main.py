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
from core.message_class import Message
# from core.log_handle import MyLog

class CvMain:
    def __init__(self,send_queue,recv_queue):
        servers.constant.SERVER_LOG = Logger(name="CV",level=LOGGER_LEVEL)
        self.log_handle = servers.constant.SERVER_LOG()
        self.send_queue = send_queue
        self.recv_queue = recv_queue
        self.Init()
        threading.Thread(target=self.test_send).start()

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

    def send_message(self,recv_server=None,obj=None,op=None,value=None):
        message = create_message(send_server=Message.CV_SERVER,recv_server=recv_server,obj=obj,op=op,value=value)
        self.send_queue.put(message)
        self.log_handle.info(f"CV -- 已发送:f{message}")

    def test_send(self):
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_LEFT)  # TODO 测试一下
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_RIGHT)
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_LEFT)
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_RIGHT)
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_LEFT)
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_RIGHT)
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_LEFT)
        # TODO 测试一下

if __name__ == '__main__':
    pass