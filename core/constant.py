#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/20:07
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : constant
# @Software: PyCharm
import json
from config.constant import MY_PATH
from core.tools import singleton



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










