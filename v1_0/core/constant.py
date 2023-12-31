#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/20:07
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : constant
# @Software: PyCharm
import json
from v1_0.config.constant import MY_PATH
from v1_0.core.tools import singleton
from queue import Queue

# 启动配置写在这   1-是 0-否

# 是否使用轻量级APP
USE_FAST_APP = 0

# 检测不到串口时是否关闭程序
NO_SERIAL_TURN_OFF = 0 # 0 是不关闭  1 是关闭

# 舵机动作间隔时间
# 调整舵机等待动作时间
# 解释：当检测到类别时，舵机开启反向动作，经过PICKER_WAITE秒后，进行分类动作
PICKER_WAITE = 3

# 通讯常量
SER_PORT = None
SER_BAUDRATE = None
SER_SEND_QUEUE = Queue()
SER_RECV_QUEUE = Queue()

# 服务名称
CV_SERVER = "CV_SERVER"
PICKER_SERVER = "PICKER_SERVER"

# 核心服务的日志管理器
CORE_LOG = None
LOGGER_LEVEL = 'debug'

@singleton
class CoreConfig:
    def __init__(self):
        #先读配置
        pass

@singleton
class ServerConfig:
    def __init__(self):
        # 读取 JSON 文件
        file_path = f"{MY_PATH}\config\software_config\software.json"
        with open(file_path, "r") as file:
            self.config = json.load(file)

        # 从 JSON 数据中提取服务信息
        software_list = self.config["software_list"]

        # 创建一个列表，用于存储所有服务的信息
        self.all_services = []

        # 遍历每个软件服务字典，提取三个属性，并合成为一个列表元素
        for software in software_list:
            software_name = software["software_name"]
            service_name = software["service_name"]
            class_name = software["class_name"]

            # 将三个属性合成一个列表元素，并添加到 all_services 列表中
            service_info = {
                "software_name":software_name,
                "service_name":service_name,
                "class_name":class_name
            }
            self.all_services.append(service_info)

# 队列数量
QUEUE_SIZE = 7










