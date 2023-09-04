#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/16/1:05
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : fast_SmartPicker
# @Software: PyCharm
import sys
import threading
import time
import camera_SDK.DaHeng.gxipy as gx
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from v1_0.servers.cv_server.constant import CvConstant
# import v1_0.fast_version.constant
from v1_0.core.communication_class import SerialCom
from multiprocessing.queues import Queue
from v1_0.core.constant import *
from v1_0.servers.cv_server.constant import *
from v1_0.core.message_class import Message
from v1_0.servers.cv_server.constant import MODEL_PATH
from v1_0.servers.picker_server.constant import CLASS_NUM_ONE, CLASS_NUM_TWO, CLASS_NUM_THREE
from v1_0.core.tools import *


@singleton
class Fast_SmartPicker:
    def __init__(self):
        v1_0.fast_version.constant.FAST_LOG= Logger(name="FAST_APP",level=LOGGER_LEVEL)
        self.log_handle = v1_0.fast_version.constant.FAST_LOG()
        self.send_queue = Queue()
        self.recv_queue = Queue()
        self.log_handle.info("FAST_APP -- 轻量化APP正在初始化")
        # Process(target=self.create_serial_conn,args=(self.send_queue,self.recv_queue)).start()
        self.create_serial_conn(send_queue=self.send_queue,recv_queue=self.recv_queue)
        self.Init()

    def Init(self):
        self.model = YOLO(model=MODEL_PATH)
        self.log_handle.info("FAST_APP -- 模型加载成功")
        self.constant_Init()
        # self.log_handle.info("FAST_APP -- ")
        threading.Thread(target=self.detect).start()

    def constant_Init(self):
        CvConstant()

    def create_serial_conn(self,send_queue,recv_queue):
        # 创建串口
        # 并执行监听任务
        SerialCom(send_queue,recv_queue)
        self.log_handle.info("FAST_APP -- 串口助手启动成功")

    def deal_classes(self,class_detect_res):
        classes_list = []
        try:
            classes_list.append(v1_0.servers.cv_server.constant.CLASSES_LIST[int(class_detect_res)])
            self.log_handle.info(f"FAST_APP -- 检测到类别{classes_list}")
            class_num = int(str(class_detect_res)[-1])
            if class_num == CLASS_NUM_ONE:
                self.send_queue.put(Message.PICKER_VALUE_CLASS_ONE_1)
                time.sleep(PICKER_WAITE)
                self.send_queue.put(Message.PICKER_VALUE_CLASS_ONE_2)
                # self.recover_picker()
            elif class_num == CLASS_NUM_TWO:
                self.send_queue.put(Message.PICKER_VALUE_CLASS_TWO_1)
                time.sleep(PICKER_WAITE)
                self.send_queue.put(Message.PICKER_VALUE_CLASS_TWO_2)
                # self.recover_picker()
            elif class_num == CLASS_NUM_THREE:
                self.send_queue.put(Message.PICKER_VALUE_CLASS_TWO_1)
                time.sleep(PICKER_WAITE)
                self.send_queue.put(Message.PICKER_VALUE_CLASS_TWO_2)
                # self.recover_picker()
        except Exception as e:
            print(e)


    def detect(self):
        self.log_handle.info("FAST_APP -- 目标检测模块启动")
        class_list = list()
        if v1_0.servers.cv_server.constant.MY_CAMERA == HAIKANG:
            pass
        elif v1_0.servers.cv_server.constant.MY_CAMERA == DAHENG:
            device_manager = gx.DeviceManager()
            dev_num, dev_info_list = device_manager.update_device_list()
            if dev_num == 0:
                sys.exit(1)
            str_index = dev_info_list[0].get("index")
            cam = device_manager.open_device_by_index(str_index)
            cam.stream_on()
            count = 0
            while True:
                raw_image = cam.data_stream[0].get_image()
                raw_image.save_raw("raw_image.raw")
                rgb_image = raw_image.convert("RGB")
                if rgb_image is None:
                    continue
                numpy_image = rgb_image.get_numpy_array()
                if numpy_image is None:
                    continue
                image = Image.fromarray(numpy_image, 'RGB')
                image_np = np.array(image)
                # Convert RGB image to BGR for OpenCV
                bgr_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

                processed_image = self.process_image(bgr_image)
                if count == 10:
                    count = 0
                    results = self.model(processed_image)
                    c = results[0].boxes.cls
                    for i in results[0].boxes.xywhn.cpu().numpy():
                        if i[1] > 0.5 and i[1] < 0.9:
                            for i in c:
                                class_list.append(int(i))
                        else:
                            # 进行检测
                            if len(class_list) > 10:
                                class_detect_res = max(class_list, key=class_list.count)
                                class_list = list()
                                self.deal_classes(class_detect_res)
                            else:
                                class_list = list()

                    # 绘制结果
                    annotated_frame = results[0].plot()
                    # 显示图像
                    cv2.imshow(winname="YOLOV8", mat=annotated_frame)
                count += 1
                # 按ESC退出
                if cv2.waitKey(1) == 27:
                    break
            # 释放连接
            cam.release()
            cv2.destroyAllWindows()
            cam.stream_off()

        elif v1_0.servers.cv_server.constant.MY_CAMERA == USB_CAMERA:
            # 摄像头编号
            # camera_nu = TEST_MP4_PATH
            camera_nu = 0
            class_list = list()
            # 打开摄像头
            cap = cv2.VideoCapture(camera_nu)
            while cap.isOpened():
                # 获取图像
                res, frame = cap.read()
                # 如果读取成功
                if res:
                    # 正向推理
                    # 图像处理
                    # processed_image = self.process_image(frame)
                    results = self.model(frame)
                    c = results[0].boxes.cls
                    for i in results[0].boxes.xywhn.cpu().numpy():
                        if i[1] > 0.5 and i[1] < 0.9:
                            for i in c:
                                class_list.append(int(i))
                        else:
                            # 进行检测
                            if len(class_list) > 10:
                                class_detect_res = max(class_list, key=class_list.count)
                                class_list = list()
                                threading.Thread(target=self.deal_classes,args=(class_detect_res,)).start()
                            else:
                                class_list = list()

                    # 绘制结果
                    annotated_frame = results[0].plot()
                    # 显示图像
                    cv2.imshow(winname="YOLOV8", mat=annotated_frame)

                    # 按ESC退出
                    if cv2.waitKey(1) == 27:
                        break
            # 释放连接
            cap.release()
            cv2.destroyAllWindows()
if __name__ == '__main__':
    Fast_SmartPicker()
