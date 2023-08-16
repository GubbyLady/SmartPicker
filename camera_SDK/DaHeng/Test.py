#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/7/17:02
# @Author  : 周伟帆
# @Project : HiKangTest
# @File    : Test
# @Software: PyCharm
import sys
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

raw_image = cam.data_stream[0].get_image()
raw_image.save_raw("raw_image.raw")

rgb_image = raw_image.convert("RGB")
if rgb_image is None:
    sys.exit(1)

numpy_image = rgb_image.get_numpy_array()
if numpy_image is None:
    sys.exit(1)

image = Image.fromarray(numpy_image, 'RGB')
image_np = np.array(image)

# Convert RGB image to BGR for OpenCV
bgr_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

# Display the image
cv2.imshow('Image', bgr_image)

# Save the image
cv2.imwrite("captured_image.jpg", bgr_image)

# Release resources
cv2.waitKey(0)
cv2.destroyAllWindows()
cam.stream_off()
