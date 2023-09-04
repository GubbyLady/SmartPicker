#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/19/21:49
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : queue_dict_test
# @Software: PyCharm
import threading
import time
from multiprocessing import Process,Queue

test_queue = Queue(100)

queue_dict = {
    "test":test_queue
}
def test_len(dict1):
    while 1:
        time.sleep(1)
        L = dict1["test"].qsize()
        print(L)

if __name__ == '__main__':
    # threading.Thread(target=test_len,args=(queue_dict,)).start()
    Process(target=test_len,args=(queue_dict,)).start()
    for i in range(100):
        time.sleep(1)
        a = 100
        queue_dict["test"].put(a)
        # print(queue_dict["test"].qsize())
        # test_queue.put(a)



