# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 21:38:43 2018

@author: Administrator
"""

# 测试框架
import unittest

# 测试类
from test_hello_data import TestHelloData
from test_hello_selenium import TestHelloSelenium
from test_hello_pptx import TestHelloPptx

if __name__ == '__main__':
    # 测试套
    suite = unittest.TestSuite()
    
    # 添加测试用例
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestHelloPptx))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestHelloSelenium))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestHelloData))

    # 执行测试用例
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)