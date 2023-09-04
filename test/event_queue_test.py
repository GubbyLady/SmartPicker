#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/19/21:31
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : event_queue_test
# @Software: PyCharm
import time
from queue import Queue

# from multiprocessing.queues import Queue

test_queue = Queue()
count = 0

def test(event):
    global count
    while 1:
        time.sleep(2)
        count += 1
        print(count)
        if count == 10:
            event.set()