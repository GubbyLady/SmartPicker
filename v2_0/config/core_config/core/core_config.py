#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/18/23:04
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : core_config
# @Software: PyCharm
from v2_0.init_config import CORE_SERVER, SERVICES_LIST


class CoreConfig:
    SERVER_NAME = CORE_SERVER
    LOG_HANDLER = None  # 日志管理器
    LOGGER_LEVEL = "debug"
    SERVER_LIST = SERVICES_LIST
