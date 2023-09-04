#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/19/0:22
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : 共享事件2
# @Software: PyCharm
import multiprocessing
import time

def worker(event):
    while True:
        print("Worker is waiting for the event.")
        event.wait()  # 等待事件被设置
        print("Worker received the event. Executing the task.")
        event.clear()  # 重置事件，以便下次等待

if __name__ == '__main__':
    event = multiprocessing.Event()  # 创建事件对象

    process = multiprocessing.Process(target=worker, args=(event,))
    process.start()

    for _ in range(5):
        time.sleep(3)  # 模拟等待一段时间

        print("Main process setting the event.")
        event.set()  # 设置事件，通知另一个进程

    process.join()  # 等待子进程完成
