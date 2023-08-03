#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:57
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : constant
# @Software: PyCharm
import logging

from core.tools import singleton
from core.tools import Loggers

@singleton
class PickerConstant:
    def __init__(self):
        logging.info("PickerConstant动态配置成功")