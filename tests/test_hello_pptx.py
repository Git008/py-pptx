# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 20:54:18 2018

@author: Administrator
"""

# 测试框架
import unittest

# PPT
from pptx import Presentation

import auto_report.hello_pptx as hello_pptx 

class TestHelloPptx(unittest.TestCase):
    _prs = None
    
    def setUp(self):
        self._prs = Presentation('../resources/template/ppt_template0.pptx')
    
    def tearDown(self):
        self._prs.save('../resources/report/数据分析报告.pptx')
        
    def test_add_all_slide_layout(self):
        hello_pptx.add_all_slide_layout(self._prs)
    
        