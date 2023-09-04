#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/18/22:54
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : core_class
# @Software: PyCharm
import multiprocessing
import sys
import threading
from multiprocessing import Process,Queue
from v2_0.config.core_config.core.core_config import CoreConfig
from v2_0.init_config import CORE_SERVER
from v2_0.utils.message_pool import MessagePool
from v2_0.utils.tools import Logger,singleton
from v2_0.config.global_config import GlobalConfig
from v2_0.communication.serial_handler import SerialCom
from v2_0.services.cv.cv_class import CvClass
from v2_0.services.picker.picker_class import PickerClass
from v2_0.utils.message_class import Message
log_handle = None
# @singleton
class CoreClass:
    def __init__(self):
        # self.core_Init()
        # self.log_handler = None
        self.serial_send_queue = Queue()
        self.serial_recv_queue = Queue()
        self.server_queue_dict = {}
        self.server_event_dict = {}

        # 初始化核心消息队列
        self.Init_queue_event()

        self.core_Init()

    def Init_queue_event(self):
        self.recv_queue = Queue()
        self.recv_event = multiprocessing.Event()
        dict_data = {
            "server_name": CoreConfig.SERVER_NAME,
            "recv_queue": self.recv_queue
        }
        self.server_event_dict[CoreConfig.SERVER_NAME] = self.recv_event
        self.server_queue_dict[CoreConfig.SERVER_NAME] = dict_data

    def message_pool_init(self):
        MessagePool(self.server_queue_dict,self.server_event_dict)

    def core_Init(self):
        # 初始化核心类
        # 初始化日志
        self.log_init()
        # 初始化通讯类
        self.comm_serial_init()
        # 初始化监听事件
        threading.Thread(target=self.listen_recv_queue).start()
        # 初始化服务
        self.server_init()
        log_handle.info("Core -- 核心初始化完成...")

    def log_init(self):
        global log_handle
        CoreConfig.LOG_HANDLER = Logger(name=CoreConfig.SERVER_NAME, level=CoreConfig.LOGGER_LEVEL)
        log_handle = CoreConfig.LOG_HANDLER()
        log_handle.info("Core -- 日志管理器初始化成功 ")

    def deal_queue_item(self,message):
        log_handle.info(f"{CoreConfig.SERVER_NAME} -- 处理信息:{message}")
        op = message.op
        value = message.value
        send_server = message.send_server
        if send_server == Message.PICKER_SERVER:
            if op == Message.CORE_OP_SERIAL:
                send_data = value
                self.send_serial(send_data)

        elif send_server == Message.CV_SERVER:
            pass

    def listen_recv_queue(self):
        while True:
            self.recv_event.wait()
            # 取出一个队列元素
            message = self.recv_queue.get()
            self.deal_queue_item(message)

    # 使用进程开启通讯服务
    def comm_serial_init(self):
        SerialCom(self.serial_send_queue,self.serial_recv_queue)

    def server_init(self):
        # 激活服务要求放入 服务名  队列字典  接收事件
        # 应先创建队列字典 以及事件字典
        for server_name in CoreConfig.SERVER_LIST:
            recv_queue = Queue()
            event = multiprocessing.Event()
            dict_data = {
                "server_name": server_name,
                "recv_queue": recv_queue
            }
            self.server_event_dict[server_name] = event
            self.server_queue_dict[server_name] = dict_data

        # 初始化消息池
        log_handle.info(f"Core -- 正在激活消息池服务")
        Process(target=self.message_pool_init).start()

        # (self,server_name,queue_dict,recv_event)
        for server_name in CoreConfig.SERVER_LIST:
            server_event = self.server_event_dict[server_name]
            log_handle.info(f"Core -- 正在激活{server_name}服务")
            # exec (f"{server_name}Class(server_name,self.server_queue_dict,server_event)")
            Process(target=self.server_run,args=(server_name,self.server_queue_dict,server_event)).start()

    def server_run(self,server_name,queue_dict,recv_event):
        exec (f"{server_name}Class(server_name,queue_dict,recv_event)")

    def send_serial(self,data):
        log_handle.info(f"Core -- 传入串口队列:{data}")
        self.serial_send_queue.put(data)


if __name__ == '__main__':
    core = CoreClass()