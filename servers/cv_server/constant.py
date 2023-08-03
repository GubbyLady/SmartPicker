#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:57
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : constant
# @Software: PyCharm
import logging
from core.tools import Loggers
from core.tools import singleton

@singleton
class CvConstant:
    def __init__(self):
        logging.info("CV动态配置成功")