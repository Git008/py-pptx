# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 20:43:49 2018

@author: Administrator
"""

# 测试框架
import unittest

import auto_report.hello_selenium as hello_selenium

class TestHelloSelenium(unittest.TestCase):
    
    def test_weixin_sogou_search(self):
        hello_selenium.weixin_sogou_search('六西格玛是个P')
    
    ''' 页面变化，代码暂时不可用
    def test_get_house365_today_info(self):
        hello_selenium.get_house365_today_info()
    '''