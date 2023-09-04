#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/20/11:26
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : picker_class
# @Software: PyCharm
import threading
import time

from v2_0.config.global_config import GlobalConfig
from v2_0.services.base_class import BaseClass
from v2_0.utils.message_class import create_message,Message
from v2_0.utils.tools import Logger


class PickerClass():
    def __init__(self,server_name,queue_dict,recv_event):
        self.server_name = server_name
        self.queue_dict = queue_dict
        self.recv_event = recv_event
        self.recv_queue = self.queue_dict[self.server_name]["recv_queue"]
        log_handler = Logger(name=self.server_name,level=GlobalConfig.LOGGER_LEVEL)
        self.log_handler = log_handler()
        self.Init()

    def Init(self):
        self.log_handler.info("初始化")
        threading.Thread(target=self.listen_recv_queue).start()

    def turn_picker(self,value):
        self.send_message(recv_server=Message.CORE_SERVER,op=Message.CORE_OP_SERIAL,
                              value=value)

    def deal_queue_item(self,message):
        self.log_handler.info(f"{self.server_name} -- 处理信息:{message}")
        op = message.op
        value = message.value
        send_server = message.send_server
        if send_server == Message.CORE_SERVER:
            pass

        elif send_server == Message.CV_SERVER:
            if op == Message.PICKER_OP_START_PICKER:
                for classA in value:
                    class_num = int(str(classA)[-1])
                    if class_num == Message.PICKER_CLASS_NUM_ONE:
                        self.turn_picker(Message.PICKER_VALUE_CLASS_ONE_1)
                        time.sleep(Message.PICKER_WAITE)
                        self.turn_picker(Message.PICKER_VALUE_CLASS_ONE_2)
                        # self.recover_picker()
                    elif class_num == Message.PICKER_CLASS_NUM_TWO:
                        self.turn_picker(Message.PICKER_VALUE_CLASS_TWO_1)
                        time.sleep(Message.PICKER_WAITE)
                        self.turn_picker(Message.PICKER_VALUE_CLASS_TWO_2)
                        # self.recover_picker()
                    elif class_num == Message.PICKER_CLASS_NUM_THREE:
                        self.turn_picker(Message.PICKER_VALUE_CLASS_TWO_1)
                        time.sleep(Message.PICKER_WAITE)
                        self.turn_picker(Message.PICKER_VALUE_CLASS_TWO_2)
                        # self.recover_picker()

    def listen_recv_queue(self):
        while True:
            self.recv_event.wait()
            # 取出一个队列元素
            message = self.recv_queue.get()
            self.deal_queue_item(message)

    def send_message(self, recv_server=None, obj=None, op=None, value=None):
        send_queue = self.queue_dict[recv_server]["recv_queue"]
        message = create_message(send_server=self.server_name,recv_server=recv_server,obj=obj,op=op,value=value)
        send_queue.put(message)

if __name__ == '__main__':
    # a = CvClass(1,2,3
    pass