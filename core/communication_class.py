#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/4/20:31
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : communication_class
# @Software: PyCharm
import json

import serial as Ser
import threading
import time
import core.constant
from core.constant import SER_PORT,SER_BAUDRATE
from config.constant import MY_PATH
from core.tools import Logger
from core.tools import singleton

# 该文件是项目的通讯类
# 目前可支持 串口通讯  mqtt（写好接口 必要可开发）
@singleton
class SerialCom:
    # 该类是串口通讯类 仍然采用先动态配置
    # 具备接收队列 发送队列
    # 该类是在CORE主服务创建，顾主要通讯仍在CORE

    def __init__(self, send_queue,recv_queue):
        try:
            self.Init()
            self.ser = Ser.Serial(core.constant.SER_PORT, core.constant.SER_BAUDRATE)
            self.send_queue = send_queue
            self.recv_queue = recv_queue
            self.connect()
            Logger().info("COM -- 串口通讯初始化成功")
            # self.SERIAL_SEND = SEND_SERIAL
            # self.SERIAL_RECEIVING = RECEIVING_SERIAL
        except Exception as e:
            Logger().error(e)
            Logger().error("COM -- 串口通讯初始化失败")

    def Init(self):
        # 动态配置
        # 读取 JSON 文件
        file_path = f"{MY_PATH}\config\communication_config\communication.json"
        with open(file_path, "r") as file:
            self.config = json.load(file)

        # 从 JSON 数据中提取服务信息
        com_list = self.config["com_list"]

        # 遍历每个软件服务字典，提取三个属性，并合成为一个列表元素
        for com in com_list:
            if com["com_name"] == "serial":
                core.constant.SER_PORT = com["port"]
                core.constant.SER_BAUDRATE = com["baudrate"]
            break

    def connect(self):
        try:
            # 先关闭再打开
            self.ser.close()
            time.sleep(0.3)
            self.ser.open()
            Logger().info("COM -- 成功启动串口")
        except Exception as e:
            Logger().error("COM -- 串口启动失败")
        try:
            threading.Thread(target=self.read_line).start()
            threading.Thread(target=self.write_line).start()
        except Exception as e:
            print(e)

    def send_message(self, message):
        pass

    def recv_message(self):
        pass

    def disconnect(self):
        pass

    def write_line(self):
        while True:
            try:
                if self.send_queue.qsize() > 0:
                    message = self.send_queue.get()
                    # print_msg = str(message)
                    self.ser.write(message.encode("utf-8"))
                    Logger().info(f"COM -- 写入串口信息:{message}")
                else:
                    pass
            except Exception as e:
                Logger().error("COM -- 串口写入失败")

    def read_line(self):
        try:
            while True:
                size = self.ser.inWaiting()
                if size != 0:
                    try:
                        response = self.ser.read(size)
                        self.recv_queue.put(response)
                        Logger().info(f"COM -- 收到串口消息:{str(response)}")
                    except Exception as e:
                        Logger().error("COM -- 读取串口数据错误" + str(e))

                    self.ser.flushInput()
                    time.sleep(0.001)
        except KeyboardInterrupt:
            self.ser.close()

class MqttCom:
    pass