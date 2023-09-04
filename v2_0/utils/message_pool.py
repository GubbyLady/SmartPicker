#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/19/21:42
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : message_pool
# @Software: PyCharm

# 这里是消息池助理
"""
消息池运作流程：
    传入 总队列字典 总任务字典
    对每条发送队列进行查看长度
    当该接收队列不为0时 ———————— 将该服务的接收任务 set 之后关闭即可
"""
import time

from v2_0.config.global_config import GlobalConfig
from v2_0.utils.tools import Logger

"""
queue_dict,event_dict
的格式：
queue_dict = {
    "服务名": {
        "server_name":Name,
        "recv_queue":Queue
        },
    "服务名2": {},
    "服务名3": {}
}

event_dict = {
    "服务名":event,
    "服务名2":event

}

"""

class MessagePool:
    def __init__(self,queue_dict,event_dict):
        log_handler = Logger(name="MessagePool", level=GlobalConfig.LOGGER_LEVEL)
        self.log_handler = log_handler()
        self.queue_dict = queue_dict
        self.event_dict = event_dict
        self.log_handler.info("MessagePool -- 消息池初始化成功")
        self.run()
    def run(self):
        while True:
            # 对发送的队列进行遍历
            # 该版本不进行转发，而是直发
            for server_queue in self.queue_dict:
                if self.queue_dict[server_queue]["recv_queue"].qsize()>0:
                    # 将对应任务set
                    event_name = server_queue
                    event = self.event_dict[event_name]
                    event.set()
                    # time.sleep(0.05)
                    event.clear()
