#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/20/11:13
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : cv_class
# @Software: PyCharm
import sys
import threading
import time

import cv2
import numpy as np
from PIL.Image import Image
from ultralytics import YOLO
import camera_SDK.DaHeng.gxipy as gx
from v2_0.config.core_config.services.cv_config import CvConfig, read_classes_file
from v2_0.config.global_config import GlobalConfig
from v2_0.services.base_class import BaseClass
from v2_0.utils.message_class import create_message,Message
from v2_0.utils.tools import Logger


class CvClass():
    def __init__(self,server_name,queue_dict,recv_event):
        self.server_name = server_name
        self.queue_dict = queue_dict
        self.recv_event = recv_event
        self.recv_queue = self.queue_dict[self.server_name]["recv_queue"]
        log_handler = Logger(name=self.server_name,level=GlobalConfig.LOGGER_LEVEL)
        self.log_handler = log_handler()
        self.Init()

    def Init(self):
        self.log_handler.info("Cv -- 正在初始化...")
        threading.Thread(target=self.listen_recv_queue).start()
        # 读取类别文件
        CvConfig.CLASSES_LIST = read_classes_file()
        # time.sleep(10)
        # self.send_message(recv_server=Message.PICKER_SERVER)
        threading.Thread(target=self.detect_run,args=(CvConfig.MODEL_PATH,)).start()
        # self.detect_run(CvConfig.MODEL_PATH)



    def deal_queue_item(self,message):
        self.log_handler.info(f"{self.server_name} -- 处理信息:{message}")
        pass

    def listen_recv_queue(self):
        while True:
            self.recv_event.wait()
            # 取出一个队列元素
            message = self.recv_queue.get()
            self.deal_queue_item(message)

    def send_message(self, recv_server=None, obj=None, op=None, value=None):
        send_queue = self.queue_dict[recv_server]["recv_queue"]
        message = create_message(send_server=self.server_name,recv_server=recv_server,obj=obj,op=op,value=value)
        send_queue.put(message)

    def open_camera(self):
        if CvConfig.DEVICE_CAMERA == CvConfig.HAIKANG:
            self.log_handler.info("CV -- 接入摄像头型号为：海康威视")
        elif CvConfig.DEVICE_CAMERA == CvConfig.DAHENG:
            self.log_handler.info("CV -- 接入摄像头型号为：大恒工业")
            # device_manager = gx.DeviceManager()
            # dev_num, dev_info_list = device_manager.update_device_list()
            # if dev_num == 0:
            #     sys.exit(1)
            # str_index = dev_info_list[0].get("index")
            # cam = device_manager.open_device_by_index(str_index)
            # return cam
        elif CvConfig.DEVICE_CAMERA == CvConfig.USB:
            self.log_handler.info("CV -- 接入摄像头型号为：USB摄像头")
            try:
                cap = cv2.VideoCapture(0)
                # cap = cv2.VideoCapture(TEST_MP4_PATH)
                return cap
            except:
                self.log_handler.info("CV -- 摄像头启动失败")

    def deal_classes(self,class_detect_res):
        classes_list = []
        try:
            # for i in classes.cpu().numpy():
            #     classes_list.append(servers.cv_server.constant.CLASSES_LIST[int(i)])
            #
            # if len(classes_list) == 0:
            #     return None
            classes_list.append(CvConfig.CLASSES_LIST[int(class_detect_res)])
            self.log_handler.info(f"CV -- 检测到类别:{classes_list}")
            self.send_message(recv_server=Message.PICKER_SERVER,op=Message.PICKER_OP_START_PICKER,value=classes_list)
        except Exception as e:
            self.log_handler.error(e)

    def process_image(self,image):
        # 降低图像分辨率
        resized_image = cv2.resize(image, None, fx=0.5, fy=0.5)

        # 应用高斯模糊
        blurred_image = cv2.GaussianBlur(resized_image, (5, 5), 0)

        return blurred_image

    def detect_run(self,model):
        # 启动摄像头
        # 加载模型
        model = YOLO(model=model)
        # 打开摄像头
        cap = self.open_camera()
        class_list = list()
        if CvConfig.DEVICE_CAMERA == CvConfig.HAIKANG:
            self.log_handler.info("CV -- 海康威视检测启动")
        elif CvConfig.DEVICE_CAMERA == CvConfig.DAHENG:
            self.log_handler.info("CV -- 大恒工业检测启动")
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

                # processed_image = self.process_image(bgr_image)
                if count == 10:
                    count = 0
                    results = model(bgr_image)
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
                count+=1
                # 按ESC退出
                if cv2.waitKey(1) == 27:
                    break
            # 释放连接
            cam.release()
            cv2.destroyAllWindows()
            cam.stream_off()

        elif CvConfig.DEVICE_CAMERA == CvConfig.USB:
            self.log_handler.info("CV -- 摄像头启动成功")
            while cap.isOpened():
                # 获取图像
                res, frame = cap.read()
                # 如果读取成功
                if res:
                    # 正向推理
                    # 图像处理
                    # processed_image = self.process_image(frame)
                    results = model(frame)
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

                    # 按ESC退出
                    if cv2.waitKey(1) == 27:
                        break
            # 释放连接
            cap.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    a = CvClass(1,2,3)