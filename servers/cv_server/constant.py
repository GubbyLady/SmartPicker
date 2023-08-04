#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:57
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : constant
# @Software: PyCharm
import logging

import servers.constant
from core.tools import Loggers
from core.tools import singleton
from servers.constant import SERVER_LOG



@singleton
class CvConstant:
    def __init__(self):
        self.log_handle = servers.constant.SERVER_LOG()
        self.log_handle.info("CV -- 动态配置成功")
        # servers.constant.SERVER_LOG
