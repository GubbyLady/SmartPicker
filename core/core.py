#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:55
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : main
# @Software: PyCharm
import logging
import threading
import time
from core.constant import ServerConfig,QUEUE_SIZE
from core.servers_class import CvServer,PickerServer
from core.tools import Redis_server,Loggers
from multiprocessing import Process,Queue
"""
该py文件运行流程
    先启动动态配置
    启动日志
    启动redis
    启动服务

"""
class CoreClass:
    #核心类：所有服务的主进程，其他服务都是其子进程
    def __init__(self):
        self.core_Init()

    def core_Init(self):
        ServerConfig()
        logging.info("服务配置动态导入成功")
        Loggers()
        Redis_server()

        # 名义上是各个服务的接收消息的队列
        # 但是子服务检测到收到的队列，就得发出去了，所以如此命名
        self.re_queue_send = {}

        # 名义上是各个服务的发送消息的队列
        # 但是子服务发送队列，这里检测到了，就得发出去了，所以如此命名
        self.send_queue_re = {}

        # 储存服务名称的列表
        self.server_names = []

        self.server_Init()

        threading.Thread(target=self.listen_send_queue).start()
        print()

    def server_process_run(self,class_name, server_name,send_queue,recv_queue):
        # 进行实例化服务操作,启动服务
        class_obj = globals()[class_name]
        print(f"{server_name}服务启动成功 (进程内启动...)")
        instance = class_obj(send_queue=send_queue, recv_queue=recv_queue)
        # logging.info(f"{server_name}服务启动成功 (进程内启动...)")

    def create_send_and_recv_queue(self):
        send_queue = Queue(QUEUE_SIZE)
        recv_queue = Queue(QUEUE_SIZE)
        return {
            "send_queue":send_queue,
            "recv_queue":recv_queue
        }

    def deal_message(self,message):
        # 对信息进行处理和提取接收方，对接收方进行发送，形成消息通路
        print(f"处理message:{message}")

    def listen_send_queue(self):
        while True:
            # 监听服务们的发送队列
            for server_name in self.server_names:
                if self.send_queue_re[server_name]["send_queue"].qsize() != 0:
                    message = self.send_queue_re[server_name]["send_queue"].get()
                    self.deal_message(message)
                    # print("接收到")
                else:
                    pass

    def server_Init(self):
        # 启动服务
        for server in ServerConfig().all_services:
            class_name = server['class_name']
            server_name = server['service_name']
            # 对每个服务创建两个队列，一个接收 一个发送
            # send_recv_queue = self.create_send_and_recv_queue()
            send_queue = Queue(QUEUE_SIZE)
            recv_queue = Queue(QUEUE_SIZE)
            self.send_queue_re[server_name] = {
                "send_queue":send_queue
            }
            self.re_queue_send[server_name] = {
                "recv_queue": recv_queue
            }
            self.server_names.append(server_name)
            p = Process(target=self.server_process_run, args=(class_name, server_name,send_queue,recv_queue,))
            p.start()

if __name__ == '__main__':
    pass
