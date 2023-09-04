#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:57
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : main
# @Software: PyCharm
import threading
import time

import v1_0.servers.constant
from v1_0.core.constant import CV_SERVER, PICKER_SERVER, LOGGER_LEVEL,PICKER_WAITE
from v1_0.core.message_class import Message,create_message
# from core.log_handle import MyLog
from v1_0.servers.picker_server.constant import PickerConstant,CLASS_NUM_ONE,CLASS_NUM_TWO,CLASS_NUM_THREE
from v1_0.servers.constant import SERVER_LOG
from v1_0.core.tools import Logger

class PickerMain:
    def __init__(self, send_queue, recv_queue):
        v1_0.servers.constant.SERVER_LOG = Logger(name="PICKER",level=LOGGER_LEVEL)
        self.log_handle = v1_0.servers.constant.SERVER_LOG()
        self.send_queue = send_queue
        self.recv_queue = recv_queue
        self.Init()

    def Init(self):
        PickerConstant()
        threading.Thread(target=self.listen_recv_queue).start()
        # self.recover_picker()
        threading.Thread(target=self.recover_picker).start()

    def recover_picker(self):
        # 将舵机恢复正位
        self.send_message(recv_server=Message.CORE_SERVER, op=Message.CORE_OP_SERIAL,
                          value=Message.PICKER_VALUE_RECOVER)
        self.log_handle.info("PICKER -- 舵机已复位")

    def deal_message(self,msg):
        # 处理消息
        if msg.op == Message.PICKER_OP_TURN_LEFT:
            self.send_message(recv_server=Message.CORE_SERVER,op=Message.CORE_OP_SERIAL,value=Message.PICKER_VALUE_LEFT)

        elif msg.op == Message.PICKER_OP_TURN_RIGHT:
            self.send_message(recv_server=Message.CORE_SERVER, op=Message.CORE_OP_SERIAL,
                              value=Message.PICKER_VALUE_RIGHT)

        elif msg.op == Message.PICKER_OP_START_PICKER:
            for classA in msg.value:
                class_num = int(str(classA)[-1])
                if class_num == CLASS_NUM_ONE:
                    self.turn_picker(Message.PICKER_VALUE_CLASS_ONE_1)
                    time.sleep(PICKER_WAITE)
                    self.turn_picker(Message.PICKER_VALUE_CLASS_ONE_2)
                    # self.recover_picker()
                elif class_num == CLASS_NUM_TWO:
                    self.turn_picker(Message.PICKER_VALUE_CLASS_TWO_1)
                    time.sleep(PICKER_WAITE)
                    self.turn_picker(Message.PICKER_VALUE_CLASS_TWO_2)
                    # self.recover_picker()
                elif class_num == CLASS_NUM_THREE:
                    self.turn_picker(Message.PICKER_VALUE_CLASS_TWO_1)
                    time.sleep(PICKER_WAITE)
                    self.turn_picker(Message.PICKER_VALUE_CLASS_TWO_2)
                    # self.recover_picker()


    def turn_picker(self,value):
        self.send_message(recv_server=Message.CORE_SERVER,op=Message.CORE_OP_SERIAL,
                              value=value)


    def listen_recv_queue(self):
        # 对接收的队列进行监听
        while True:
            if self.recv_queue.qsize() != 0:
                # 接收队列不为空
                recv_msg = self.recv_queue.get()
                self.log_handle.info(f"PICKER -- 收到信息:{recv_msg}")
                threading.Thread(target=self.deal_message,args=(recv_msg,)).start()
                # self.deal_message(recv_msg)
            else:
                pass

    def send_message(self,recv_server=None,obj=None,op=None,value=None):
        message = create_message(send_server=Message.PICKER_SERVER, recv_server=recv_server, obj=obj, op=op, value=value)
        self.send_queue.put(message)
        self.log_handle.info(f"PICKER -- 已发送:f{message}")


if __name__ == '__main__':
    # print("picker服务启动")
    pass