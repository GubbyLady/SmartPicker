#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/18/23:09
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : global_config
# @Software: PyCharm
import os

# 该文件书写全局的配置

class GlobalConfig:
    LOGGER_LEVEL = 'debug'  # 日志过滤

    # 项目路径
    BASE_PATH = os.path.abspath("")