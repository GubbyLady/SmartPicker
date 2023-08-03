#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/4/0:14
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : message_class
# @Software: PyCharm

class Message:
    # 信息通讯的核心类
    def __init__(self,send_server,recv_queue,obj,op,value):
        self.send_server = send_server
        self.recv_server = recv_queue
        self.obj = obj
        self.op = op
        self.value = value

    def __str__(self):
        return f'发送方:{self.send_server}、接收方:{self.recv_server}、目标对象:{self.obj}、操作:{self.op}、值:{self.value}  '

def create_message(send_server,recv_server,obj,op,value):
    return Message(send_server,recv_server,obj,op,value)

