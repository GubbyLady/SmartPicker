#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/19/0:52
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : redis测试2
# @Software: PyCharm
import redis
import pickle

class IMessage:
    def __init__(self, content):
        self.content = content

def store_instance(redis_client, key, instance):
    serialized_instance = pickle.dumps(instance)  # 序列化对象
    redis_client.set(key, serialized_instance)

def retrieve_instance(redis_client, key):
    serialized_instance = redis_client.get(key)
    if serialized_instance:
        instance = pickle.loads(serialized_instance)  # 反序列化对象
        return instance
    else:
        return None

if __name__ == '__main__':
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    # 存储类实例
    message_instance = IMessage("Hello from Python!")
    store_instance(redis_client, 'my_instance', message_instance)

    # 获取类实例
    retrieved_instance = retrieve_instance(redis_client, 'my_instance')
    if retrieved_instance:
        print("Retrieved content of instance:", retrieved_instance)
    else:
        print("Instance not found.")
