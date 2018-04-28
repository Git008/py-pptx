# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 21:20:00 2018

@author: Administrator
"""

# 测试框架
import unittest

from auto_report.hello_data import HelloData

class TestHelloData(unittest.TestCase):
    _hello_data = None
    
    def __init__(self, methodName):
        super(TestHelloData, self).__init__(methodName)
        
        # 导入数据集
        self._hello_data = HelloData('../resources/data/data0.xlsx', 'Sheet1')
        
    def test_seaborn_boxplot1(self):
        self._hello_data.seaborn_boxplot1()
        
    def test_seaborn_boxplot2(self):
        self._hello_data.seaborn_boxplot2()
        
    def test_seaborn_boxplot3(self):
        self._hello_data.seaborn_boxplot3()
        
    def test_seaborn_pointplot(self):
        self._hello_data.seaborn_pointplot()
        
    def test_seaborn_stripplot(self):
        self._hello_data.seaborn_stripplot()       
        
    def test_df_pivot_table(self):
        self._hello_data.df_pivot_table()        