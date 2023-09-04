#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:50
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : tools
# @Software: PyCharm

"""
配置文件注入
"""
import logging
from abc import abstractmethod
import datetime

from nb_log import get_logger

import v1_0.core.constant
from v1_0.config.constant import MY_PATH


# from core.constant import CORE_LOG

class Tools(object):

    @abstractmethod
    def Init(self):
        pass

    @abstractmethod
    def run(self):
        pass


# 单例模式装饰器
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

class Redis_server:
    def __init__(self):
        logging.info("Redis数据库启动")

def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

class Loggers:
    def __init__(self):
        log_filename = f"{MY_PATH}\log\{get_current_date()}_log.log"
        logging.basicConfig(filename=log_filename, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        # 创建一个StreamHandler，并设置其日志级别为INFO
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 创建一个Formatter，用于设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # 将Formatter添加到StreamHandler
        console_handler.setFormatter(formatter)

        # 将StreamHandler添加到根logger
        logging.getLogger().addHandler(console_handler)

        logging.info("日志初始化成功")

    def log(self, level, message):
        if level == 'info':
            logging.info(message)
        elif level == 'error':
            logging.error(message)
        elif level == 'warning':
            logging.warning(message)
        else:
            logging.debug(message)
# # 使用单例类记录日志
# logger = LoggerSingleton()
# logger.log('info', 'This is an information message.')
# logger.log('error', 'An error occurred.')
# Loggers()


class Logger(object):
    """
    日志类
    """
    __isinstance = False

    def __new__(cls, *args, **kwargs):
        if cls.__isinstance:  # 如果被实例化了
            return cls.__isinstance.logger  # 返回实例化对象
        cls.__isinstance = object.__new__(cls)  # 否则实例化
        return cls.__isinstance  # 返回实例化的对象

    def __init__(self, **kwargs):
        self.logger = get_logger(name=kwargs.get("name"), log_path=v1_0.core.constant.MY_PATH + "\\log",
                                 log_filename="SmartPicker_log.log")

    def __call__(self, *args, **kwargs):
        return self.logger

