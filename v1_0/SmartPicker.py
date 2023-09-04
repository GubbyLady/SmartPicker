#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/3/23:47
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : SmartPicker
# @Software: PyCharm
from core.core_class import CoreClass
from fast_version.fast_SmartPicker import Fast_SmartPicker
from core.constant import USE_FAST_APP

if __name__ == '__main__':
    if USE_FAST_APP:
        Fast_SmartPicker()
    else:
        coreApp = CoreClass()
