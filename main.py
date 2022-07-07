# @Author: chenrw
# -*- coding:utf-8 -*-
# @Time: 2020-4-3 8:49
# @File: main.py
import HTMLTestRunner_cn
import unittest
from common_data.dir_path import *

if __name__ == '__main__':
    # 判断保存报告的路径是否存在，没有则新建
    isExist = os.path.exists(ReportPath)
    if not isExist:
        os.makedirs(ReportPath)
    # 报告名称
    report_name = os.path.join(ReportPath, '%s_Report.html' % (time.strftime('%m_%d_%H_%M')))
    discover = unittest.defaultTestLoader.discover(TestCase_path,
                                                   pattern="Test_*.py",
                                                   top_level_dir=TestCase_path)
    runner = HTMLTestRunner_cn.HTMLTestRunner(title="自动化测试报告",
                                              description="测试结果",
                                              stream=open(report_name, "wb"),
                                              verbosity=2,
                                              retry=0)
    runner.run(discover)

