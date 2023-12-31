#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:57
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : constant
# @Software: PyCharm
import logging
import v1_0.servers.constant
from v1_0.core.tools import singleton
from v1_0.core.tools import Loggers

CLASS_NUM_ONE = 1
CLASS_NUM_TWO = 2
CLASS_NUM_THREE = 3

@singleton
class PickerConstant:
    def __init__(self):
        self.log_handle = v1_0.servers.constant.SERVER_LOG()
        self.log_handle.info("PICKER -- 动态配置成功")