#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/7/17:02
# @Author  : 周伟帆
# @Project : HiKangTest
# @File    : Test
# @Software: PyCharm
import sys
import time
import cv2
from PIL import Image
import numpy as np
from ultralytics import YOLO

import camera_SDK.DaHeng.gxipy as gx
device_manager = gx.DeviceManager()
dev_num, dev_info_list = device_manager.update_device_list()
if dev_num == 0:
    sys.exit(1)
str_index = dev_info_list[0].get("index")
cam = device_manager.open_device_by_index(str_index)
cam.stream_on()
# 加载模型
model = YOLO(model="D:/pyProject/pythonProject/SmartPicker/servers/cv_server/my_detect/models/building_block.pt")
class_list = list()
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
    # Display the image
    results = model(bgr_image)
    c = results[0].boxes.cls
    for i in results[0].boxes.xywhn.cpu().numpy():
        if i[1] > 0.5 and i[1] < 0.9:
            for i in c:
                class_list.append(int(i))
        else:
            # 进行检测
            if len(class_list) > 10:
                classA = max(class_list, key=class_list.count)
                class_list = list()
                check = True
                print(classA)
            else:
                class_list = list()

    # print(class_list)
    # person_num = len(results[0])

    # 绘制结果
    annotated_frame = results[0].plot()
    # 显示图像
    cv2.imshow(winname="YOLOV8", mat=annotated_frame)

    # 按ESC退出
    if cv2.waitKey(1) == 27:
        break
# 释放连接
cam.release()
cv2.destroyAllWindows()

# Release resources
cv2.destroyAllWindows()
cam.stream_off()
