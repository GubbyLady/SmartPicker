#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/20/10:56
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : cv_config
# @Software: PyCharm
from v2_0.config.global_config import GlobalConfig
from v2_0.init_config import *
from v2_0.utils.tools import *

class CvConfig:

    LOGGER_LEVEL = "debug"
    DEVICE_CAMERA = device_camera
    HAIKANG = "HAIKANG"
    DAHENG = "DAHENG"
    USB = "USB"

    # 类别列表
    CLASSES_LIST = []

    # 模型路径
    MODEL_PATH = f"{GlobalConfig.BASE_PATH}/config/model/building_block.pt"

    # 类别文件路径
    CLASSES_FILE_PATH = f"{GlobalConfig.BASE_PATH}/config/model/classes/classes.txt"

    # 测试图片列表
    TEST_IMG_LIST = []

    # 测试图片文件夹路径
    TEST_IMG_PATH = "servers/cv_server/my_detect/test_video/img"

    # 测试视频路径
    TEST_MP4_PATH = "servers/cv_server/my_detect/test_video/mp4/1.mp4"

    def Init_img_list(self):
        global TEST_IMG_LIST
        import os
        # 遍历文件夹中的文件
        for filename in os.listdir(CvConfig.TEST_IMG_PATH):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                img_path = os.path.join(CvConfig.TEST_IMG_PATH, filename)
                TEST_IMG_LIST.append(img_path)

# 读取类别文件
def read_classes_file():
    # 打开class.txt文件
    try:
        with open(CvConfig().CLASSES_FILE_PATH, "r") as file:
            # 读取文件的每一行，并去除换行符
            class_list = [line.strip() for line in file.readlines()]
        # log_handle.info("CV -- 读取类别文本成功")
        return class_list
    except Exception as e:
        # log_handle.error(e)
        print(e)

