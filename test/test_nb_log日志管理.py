#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/4/13:21
# @Author  : 周伟帆
# @Project : SmartPicker
# @File    : test_nb_log日志管理
# @Software: PyCharm
'''
安装nb_log模块
pip
install
nb_log

1、功能介绍
(1).自动转换功能
只要import
nb_log，项目所有地方的print自动显示并在控制台可点击精确跳转到print的地方。

(2).兼容性
使用的是python内置的logging封装的，返回的logger对象的类型是py官方内置日志的Logger类型。

(3).日志记录到多个敌方
内置了一键入参，每个参数是独立开关，可以把日志同时记录到8个常用的敌方的任意几种组合，
包括：控制台、文件、钉钉、邮件、mongo、kafka、es等等。

(4).日志命名空间独立
采用了多实例logger，按日志命名空间区分。
命名空间独立意味着每个logger单独的日志级别过滤，单独的控制要记录到哪些地方。
如：

logger_aa = LogManaer("aa").get_logger_and_add_handlers(10, log_filename='aa.log')
logger_bb = LogManaer("bb").get_logger_and_add_handlers(20, log_filename='bb.log')
logger_cc = LogManaer("cc").get_logger_and_add_handlers(30, log_filename='cc.log', is_add_stream_handlers=False,
                                                        ding_talk_toker='your_dingding_toker')
'''
from nb_log import LogManager
from nb_log.handlers import ColorHandler


class TestLog:

    # 测试日志不会输出到控制台
    def testLogWithoutHandler(self):
        my_log = LogManager("my_log").get_logger_without_handlers()
        print("这条日志会打印")
        my_log.info("这条日志不会打印")

    # 测试日志级别控制输出
    def testLogLervel(self):
        my_log = LogManager("my_log").get_logger_and_add_handlers(log_level_int=20)
        """
        日志输出级别，设置为 1 2 3 4 5，分别对应原生logging.DEBUG(10)，logging.INFO(20)，
        logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，
        现在可以直接用10 20 30 40 50了，兼容了
        """
        my_log.debug("debug级别日志不会打印")
        my_log.info("info级别日志会打印")

    # 测试日志信息写入到文件
    def testWriteLogtoFile(self):
        my_log = LogManager("fm").get_logger_and_add_handlers(log_path=".", log_filename="my_log.log")
        """
        log_filename: 日志的名字，仅当log_path和log_filename都不为None时候才写入到日志文件
        """
        my_log.info("这条日志写入到日志文件my_log.log")

        """
        2022-01-26 18:06:45 - fm - "D:/pythonProject_hdc/HDC_TEST_two/Testpy/logUtil.py:16" - <module> - INFO - �[0;30;46m这条日志写入到日志文件my_log.log�[0m
        由日志内容得出，带有�[0m字样，是因为默认采用了color彩色日志
        """

        my_log = LogManager("fm").get_logger_and_add_handlers(log_path=".", log_filename="my_log.log",
                                                              do_not_use_color_handler=True)
        my_log.info("这条日志写入到日志文件my_log.log")
        """
        2022-01-26 18:11:20 - fm - "D:/pythonProject_hdc/HDC_TEST_two/Testpy/logUtil.py:16" - <module> - INFO - 这条日志写入到日志文件my_log.log
        由日志内容得出，禁用color彩色日志，日志内容不再显示�[0m字样
        """

        my_log = LogManager("fm").get_logger_and_add_handlers(log_path=".", log_filename="my_log.log",
                                                              do_not_use_color_handler=True, formatter_template=1)
        my_log.info("这条日志写入到日志文件my_log.log")
        """
        formatter_template=1 表示采用详细模板
        日志内容为：
        日志时间【2022-01-26 18:13:28】 - 日志名称【fm】 - 文件【logUtil.py】 - 第【18】行 - 日志等级【INFO】 - 日志信息【test01】

        formatter_template=2 表示采用简要模板
        日志内容为：
        2022-01-26 18:13:10 - fm - logUtil.py - <module> - 18 - INFO - test01

        formatter_template=5 表示采用最好模板（默认为最好模板）
        日志内容为：
        2022-01-26 18:13:59 - fm - "D:/pythonProject_hdc/HDC_TEST_two/Testpy/logUtil.py:18" - <module> - INFO - test01
        """

    # 测试日志写入到邮箱
    def testWriteLogtoMail(self):
        """
        将is_add_mail_handler=True打开
        同时修改nb_log_config_default中的邮箱配置
        EMAIL_HOST = ('smtp.sohu.com', 465)
        EMAIL_FROMADDR = 'aaa0509@sohu.com'  # 'matafyhotel-techl@matafy.com',
        EMAIL_TOADDRS = ('cccc.cheng@silknets.com', 'yan@dingtalk.com',)
        EMAIL_CREDENTIALS = ('aaa0509@sohu.com', 'abcdefg')
        """
        my_log = LogManager("my_log").get_logger_and_add_handlers(is_add_mail_handler=True)
        my_log.info("这条日志会发送到指定邮箱")

    # 测试日志发送到钉钉
    def testSendLogtoDingding(self):
        my_log = LogManager("my_log").get_logger_and_add_handlers(ding_talk_token="your dingding toker")
        my_log.info("这条日志会发送到钉钉")

    # 测试删除handlers
    def testRemoverHandlers(self):
        my_log = LogManager("my_log").get_logger_and_add_handlers()
        my_log.info("去除ColerHandler之前，此条日志会打印")
        LogManager("my_log").remove_handler_by_handler_class(ColorHandler)
        my_log.info("去除ColorHander之后，此条日志不会打印")

    # 测试日志写入mongo
    def testLogWritetoMongo(self):
        my_log = LogManager("my_log").get_logger_and_add_handlers(mongo_url="your mongo url", formatter_template=1)
        """
        formatter_template :日志模板，1为formatter_dict的详细模板，2为简要模板,5为最好模板
        """
        my_log.info("这条日志写入到Mongo")


testlog = TestLog()

# 测试日志不会输出到控制台
testlog.testLogWithoutHandler()
"""
结果：
15:00:29  "D:/pythonProject_hdc/HDC_TEST_two/Testpy/testNB_LOG.py:13"   这条日志会打印
"""

# 测试日志级别控制输出
testlog.testLogLervel()
"""
结果：
2022-01-04 15:02:03 - my_log - "D:/pythonProject_hdc/HDC_TEST_two/Testpy/testNB_LOG.py:26" - testLogLervel - INFO - info级别日志会打印
"""

# 测试日志信息写入到文件
testlog.testWriteLogtoFile()
"""
结果：
控制台：
22-01-04 15:05:00 - my_log - "D:/pythonProject_hdc/HDC_TEST_two/Testpy/testNB_LOG.py:35" - testWriteLogtoFile - INFO - 这条日志写入到日志文件my_log.log

日志文件：
2022-01-04 15:05:00 - my_log - "D:/pythonProject_hdc/HDC_TEST_two/Testpy/testNB_LOG.py:35" - testWriteLogtoFile - INFO - �[0;30;46m这条日志写入到日志文件my_log.log�[0m
"""

# 测试删除handlers
testlog.testRemoverHandlers()
"""
结果：
2022-01-04 15:06:12 - my_log - "D:/pythonProject_hdc/HDC_TEST_two/Testpy/testNB_LOG.py:61" - testRemoverHandlers - INFO - 去除ColerHandler之前，此条日志会打印
"""
