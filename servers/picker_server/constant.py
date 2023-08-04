#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:57
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : constant
# @Software: PyCharm
import logging

import servers.constant
from core.tools import singleton
from core.tools import Loggers

@singleton
class PickerConstant:
    def __init__(self):
        self.log_handle = servers.constant.SERVER_LOG()
        self.log_handle.info("PICKER -- 动态配置成功")