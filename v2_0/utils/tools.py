#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/18/22:54
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : tools
# @Software: PyCharm
import datetime
from nb_log import get_logger

from v2_0.config.utils_config.utils_config import UtilsConfig


# 单例模式装饰器
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

# 得到当前时间并按指定格式返回
def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# 日志类
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
        self.logger = get_logger(name=kwargs.get("name"), log_path=UtilsConfig.MY_PATH + "\\log",
                                 log_filename="SmartPicker_v2.0_log.log")

    def __call__(self, *args, **kwargs):
        return self.logger

