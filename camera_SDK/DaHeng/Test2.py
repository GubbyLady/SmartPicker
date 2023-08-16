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
import gxipy as gx
device_manager = gx.DeviceManager()
dev_num, dev_info_list = device_manager.update_device_list()
if dev_num == 0:
    sys.exit(1)
str_index = dev_info_list[0].get("index")
cam = device_manager.open_device_by_index(str_index)
cam.stream_on()

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
    cv2.imshow('Video', bgr_image)
    # Exit loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
cam.stream_off()
