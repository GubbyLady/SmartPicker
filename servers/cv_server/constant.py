#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31/19:57
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : constant
# @Software: PyCharm
import json
import logging

import fast_version.constant
import servers.constant
from core.tools import Loggers
from core.tools import singleton
from servers.constant import SERVER_LOG
from core.constant import USE_FAST_APP

# 摄像机的型号
HAIKANG = "haikang"
DAHENG = "daheng"
USB_CAMERA = "usb_camera"
MY_CAMERA = None

# 配置文件路径
CONFIG_PATH = "config/software_config/cv_config/cv.json"

# 类别列表
CLASSES_LIST = []

# 模型路径
MODEL_PATH = "servers/cv_server/my_detect/models/building_block.pt"

# 类别文件路径
CLASSES_FILE_PATH = "servers/cv_server/my_detect/classes/classes.txt"

# 测试图片列表
TEST_IMG_LIST = []

# 测试图片文件夹路径
TEST_IMG_PATH = "servers/cv_server/my_detect/test_video/img"

# 测试视频路径
TEST_MP4_PATH = "D:/pyProject/pythonProject/SmartPicker/servers/cv_server/my_detect/test_video\mp4/1.mp4"

def Init_img_list():
    global TEST_IMG_LIST
    import os
    # 遍历文件夹中的文件
    for filename in os.listdir(TEST_IMG_PATH):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(TEST_IMG_PATH, filename)
            TEST_IMG_LIST.append(img_path)

# 读取类别文件
def read_classes_file(log_handle):
    global CLASSES_LIST
    # 打开class.txt文件
    try:
        with open(CLASSES_FILE_PATH, "r") as file:
            # 读取文件的每一行，并去除换行符
            CLASSES_LIST = [line.strip() for line in file.readlines()]
        log_handle.info("CV -- 读取类别文本成功")
    except Exception as e:
        log_handle.error(e)


@singleton
class CvConstant:
    def __init__(self):
        global MY_CAMERA
        # 读取 JSON 文件
        file_path = CONFIG_PATH
        with open(file_path, "r") as file:
            self.config = json.load(file)
        MY_CAMERA = self.config["camera_name"]
        if USE_FAST_APP:
            self.log_handle = fast_version.constant.FAST_LOG()
        else:
            self.log_handle = servers.constant.SERVER_LOG()
        read_classes_file(self.log_handle)
        Init_img_list()
        self.log_handle.info("CV -- 动态配置成功")
        # servers.constant.SERVER_LOG


if __name__ == '__main__':
    cv = CvConstant()

