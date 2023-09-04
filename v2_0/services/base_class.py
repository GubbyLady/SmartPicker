#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/20/10:45
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : base_class
# @Software: PyCharm
from v2_0.utils.tools import Logger
from abc import ABC, abstractmethod
from v2_0.config.global_config import GlobalConfig

# 创建抽象类
class BaseAbc(ABC):
    def __init__(self,server_name,queue_dict,recv_event):
        self.server_name = server_name
        self.queue_dict = queue_dict
        self.recv_event = recv_event
        self.recv_queue = self.queue_dict[self.server_name]["recv_queue"]
        log_handler = Logger(name=self.server_name,level=GlobalConfig.LOGGER_LEVEL)
        self.log_handler = log_handler()
        self.Init()

    @abstractmethod
    def Init(self):
        pass

    @abstractmethod
    def deal_queue_item(self):
        # 处理接收到的消息
        pass

    @abstractmethod
    def listen_recv_queue(self):
        # 接收消息
        pass

    @abstractmethod
    def send_message(self,recv_server=None,obj=None,op=None,value=None):
        # 发送消息
        # message = create_message(send_server=Message.CV_SERVER,recv_server=recv_server,obj=obj,op=op,value=value)
        # self.send_queue.put(message)
        # self.log_handle.info(f"CV -- 已发送:f{message}")
        pass

# 创建父类
class BaseClass(BaseAbc):

    def Init(self):
        pass

    def deal_queue_item(self):
        pass

    def listen_recv_queue(self):
        pass

    def send_message(self, recv_server=None, obj=None, op=None, value=None):
        pass