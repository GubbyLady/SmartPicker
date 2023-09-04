#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/19/0:18
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : 共享事件
# @Software: PyCharm

import multiprocessing
import time
from event_queue_test import test

def process_a(event_dict):
    event = event_dict["event"]
    print("Process A is waiting for the event.")
    event.wait()
    print("Process A received the event. Executing the task.")

def process_b(event_dict):
    event = event_dict["event"]
    time.sleep(5)  # 模拟一段时间后满足条件
    print("Process B is setting the event.")
    time.sleep(2)
    event.set()




if __name__ == '__main__':
    event = multiprocessing.Event()  # 创建共享事件对象
    #
    # event_dict = {
    #     "event":event
    # }
    #
    # process_a_obj = multiprocessing.Process(target=process_a, args=(event_dict,))
    # process_b_obj = multiprocessing.Process(target=process_b, args=(event_dict,))
    #
    # process_a_obj.start()
    # process_b_obj.start()

    # process_a_obj.join()
    # process_b_obj.join()
    multiprocessing.Process(target=test,args=(event,)).start()
    print("开始等待")
    event.wait()
    print("事件发生")
