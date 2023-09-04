#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/18/22:37
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : init_config
# @Software: PyCharm

# 这里是首次启动时要进行编辑的配置文件 文件

# 通讯服务
# 串口配置
serial_port = "COM$"  # 串口端口
serial_baudrate = 9600  # 波特率
no_serial_turn_off = 0 # 检测不到串口时是否关闭强制程序

# mqtt:供远程控制的接口
mqtt_host = None  # mqtt服务器地址
mqtt_port = None  # 端口号
mqtt_admin = None  # 用户名
mqtt_password = None # 密码

# 检测设备配置
CAMERA_DICT = {
    "1":"USB",
    "2":"DAHENG",
    "3":"HAIKANG"
}

MY_CAMERA = 1  #填写 CAMERA_DICT 的 key 即可
device_camera = CAMERA_DICT[str(MY_CAMERA)]

# 舵机动作间隔时间
# 调整舵机等待动作时间
picker_run_time = 2 # 解释：当检测到类别时，舵机开启反向动作，经过PICKER_RUN_TIME秒后，进行分类动作

# 服务列表:无需修改
CORE_SERVER = "Core"
CV_SERVER = "Cv"
PICKER_SERVER = "Picker"
SERVICES_LIST = [CV_SERVER,PICKER_SERVER]