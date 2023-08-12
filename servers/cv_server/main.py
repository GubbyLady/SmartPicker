#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:57
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : main
# @Software: PyCharm
import threading
import time

import numpy as np
from PIL import Image

import servers.constant
from servers.cv_server.constant import CvConstant,MY_CAMERA,HAIKANG,DAHENG,USB_CAMERA,CLASSES_LIST,MODEL_PATH,TEST_IMG_LIST
from core.tools import Logger
from core.constant import CV_SERVER,PICKER_SERVER,LOGGER_LEVEL
from core.message_class import create_message
from servers.constant import SERVER_LOG
from core.message_class import Message
# from core.log_handle import MyLog
from ultralytics import YOLO
import cv2

# CV 模块的任务 就是运行目标检测
# 检测到物体：发送对应指令

class CvMain:
    def __init__(self,send_queue,recv_queue):
        servers.constant.SERVER_LOG = Logger(name="CV",level=LOGGER_LEVEL)
        self.log_handle = servers.constant.SERVER_LOG()
        self.send_queue = send_queue
        self.recv_queue = recv_queue
        self.Init()
        # threading.Thread(target=self.test_send).start()
        threading.Thread(target=self.detect_run,args=(MODEL_PATH,)).start()

    def Init(self):
        self.class_count = 0 # 类别计数器
        self.last_classes_list = None # 上一次类别
        self.cur_clasees_list = None
        CvConstant()
        threading.Thread(target=self.listen_recv_queue).start()

        # time.sleep(10)
        # self.send_message()

    def listen_recv_queue(self):
        # 对接收的队列进行监听
        while True:
            if self.recv_queue.qsize() != 0:
                # 接收队列不为空
                self.log_handle.info(self.recv_queue.get())
            else:
                pass

    def open_camera(self):
        if servers.cv_server.constant.MY_CAMERA == HAIKANG:
            self.log_handle.info("CV -- 接入摄像头型号为：海康威视")
        elif servers.cv_server.constant.MY_CAMERA == DAHENG:
            self.log_handle.info("CV -- 接入摄像头型号为：大恒工业")
        elif servers.cv_server.constant.MY_CAMERA == USB_CAMERA:
            self.log_handle.info("CV -- 接入摄像头型号为：USB摄像头")
            try:
                # return cv2.VideoCapture(0)
                return cv2.VideoCapture("servers/cv_server/my_detect/test_video/1.mp4")
            except:
                self.log_handle.info("CV -- 摄像头启动失败")

    def deal_classes(self,classes):
        classes_list = []
        try:
            for i in classes.cpu().numpy():
                classes_list.append(servers.cv_server.constant.CLASSES_LIST[int(i)])

            if len(classes_list) == 0:
                return None
            self.log_handle.info(f"CV -- 检测到类别:{classes_list}")
            self.send_message(recv_server=PICKER_SERVER,op=Message.PICKER_OP_START_PICKER,value=classes_list)
        except Exception as e:
            self.log_handle.error(e)


    def detect_run(self,model):
        # 启动摄像头
        # 加载模型
        model = YOLO(model=model)
        # 打开摄像头
        cap = self.open_camera()
        # self.log_handle.info("CV -- 摄像头启动成功")
        # while cap.isOpened():
        #     # 获取图像
        #     res, frame = cap.read()
        #     # 如果读取成功
        #     if res:
        #         # 正向推理
        #         results = model(frame)
        #         # 处理结果
        #         classes = results[0].boxes.cls
        #         self.deal_classes(classes)
        #
        # # 释放连接
        # cap.release()

        image_paths = servers.cv_server.constant.TEST_IMG_LIST
        target_size = (96,96)
        for image_path in image_paths:
            # 读取图片
            frame = cv2.imread(image_path)
            # 缩放图片到目标尺寸
            # resized_frame = cv2.resize(frame, target_size)
            # 正向推理
            results = model(frame)
            c = results[0].boxes.cls
            self.deal_classes(c)
            # time.sleep(2)
            # 绘制结果
            annotated_frame = results[0].plot()
            annotated_frame = cv2.resize(annotated_frame,(600,600))
            # 显示图像
            cv2.imshow(winname="YOLOV8", mat=annotated_frame)

            # 按ESC退出
            if cv2.waitKey(1) == 27:
                break
            time.sleep(5)

        # 关闭窗口
        # cv2.destroyAllWindows()

    def send_message(self,recv_server=None,obj=None,op=None,value=None):
        message = create_message(send_server=Message.CV_SERVER,recv_server=recv_server,obj=obj,op=op,value=value)
        self.send_queue.put(message)
        self.log_handle.info(f"CV -- 已发送:f{message}")

    def test_send(self):
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_LEFT)  # TODO 测试一下
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_RIGHT)
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_LEFT)
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_RIGHT)
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_LEFT)
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_RIGHT)
        time.sleep(2)
        self.send_message(recv_server=Message.PICKER_SERVER, op=Message.PICKER_OP_TURN_LEFT)


if __name__ == '__main__':
    pass