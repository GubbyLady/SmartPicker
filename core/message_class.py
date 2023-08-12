#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/4/0:14
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : message_class
# @Software: PyCharm

# 后期需要将message的规范写进此处，为了信息体系完善，后期写规范

class Message:
    # 在此处写下信息协议规范
    # 服务名称
    CORE_SERVER= "CORE"
    CV_SERVER = "CV_SERVER"
    PICKER_SERVER = "PICKER_SERVER"

    # CORE 服务的信息协议
    CORE_OP_SERIAL = "send_serial"

    # CV 服务的信息协议


    # PICKER 服务的信息协议
    PICKER_CONFIG_IO = 8

    PICKER_OP_TURN_LEFT = "turn_left"
    PICKER_OP_TURN_RIGHT = "turn_right"
    PICKER_OP_DEG = "deg"
    PICKER_OP_TIME = "time"
    PICKER_OP_START_PICKER = "start"

    PICKER_VALUE_LEFT = f"#{PICKER_CONFIG_IO}P500T10\r\n"
    PICKER_VALUE_RIGHT = f"#{PICKER_CONFIG_IO}P2500T10\r\n"
    PICKER_VALUE_RECOVER = f"#{PICKER_CONFIG_IO}P1500T10\r\n"
    PICKER_VALUE_CLASS_ONE = f"#{PICKER_CONFIG_IO}P800T10\r\n"
    PICKER_VALUE_CLASS_TWO = f"#{PICKER_CONFIG_IO}P1600T10\r\n"
    PICKER_VALUE_CLASS_THREE = f"#{PICKER_CONFIG_IO}P2400T10\r\n"

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

