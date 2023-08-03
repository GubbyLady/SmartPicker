#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/4/1:23
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : test_共享队列
# @Software: PyCharm
from multiprocessing import Process, Queue

def producer(queue):
    print(queue)
    for i in range(10):
        queue.put(i)
        print(f'Producer put: {i}')

def consumer(queue):
    print(queue)
    while True:
        item = queue.get()
        if item is None:
            break
        print(f'Consumer got: {item}')

if __name__ == '__main__':
    queue = Queue()
    print(queue)
    # 创建生产者进程
    p1 = Process(target=producer, args=(queue,))
    # 创建消费者进程
    p2 = Process(target=consumer, args=(queue,))

    # 启动进程
    p1.start()
    p2.start()

    # 等待生产者进程结束
    p1.join()

    # 在队列中放入一个空值作为停止信号
    queue.put(None)

    # 等待消费者进程结束
    p2.join()
