# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 21:20:00 2018

@author: Administrator
"""
from __future__ import annotations

import os
from typing import Optional, TYPE_CHECKING

import matplotlib
matplotlib.use('Agg')

import unittest

from auto_report.hello_data import HelloData

if TYPE_CHECKING:
    from matplotlib.figure import Figure

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(PROJECT_ROOT, 'resources')
DATA_DIR = os.path.join(RESOURCES_DIR, 'data')


class TestHelloData(unittest.TestCase):
    """
    测试 HelloData 类的功能。
    
    测试数据可视化方法，包括箱线图、散点图、折线图等。
    """
    
    _hello_data: Optional[HelloData] = None
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        在测试类开始前初始化测试数据。
        
        使用 unittest 的 setUpClass 替代 __init__，这是 unittest 的推荐做法。
        """
        data_path = os.path.join(DATA_DIR, 'data0.xlsx')
        cls._hello_data = HelloData(data_path, 'Sheet1')
    
    def setUp(self) -> None:
        """
        在每个测试方法开始前运行。
        
        确保数据已正确加载。
        """
        if self._hello_data is None or self._hello_data.dataframe is None:
            self.fail("测试数据未正确加载")
    
    def test_seaborn_boxplot1(self) -> None:
        """
        测试 seaborn_boxplot1 方法。
        
        测试使用列名方式绘制箱线图的功能。
        """
        self.assertIsNotNone(self._hello_data)
        
        try:
            fig = self._hello_data.seaborn_boxplot1()
            self.assertIsNotNone(fig)
        except Exception as e:
            self.fail(f"seaborn_boxplot1 执行失败: {e}")
        
    def test_seaborn_boxplot2(self) -> None:
        """
        测试 seaborn_boxplot2 方法。
        
        测试使用 Series 方式绘制箱线图的功能。
        """
        self.assertIsNotNone(self._hello_data)
        
        try:
            fig = self._hello_data.seaborn_boxplot2()
            self.assertIsNotNone(fig)
        except Exception as e:
            self.fail(f"seaborn_boxplot2 执行失败: {e}")
        
    def test_seaborn_boxplot3(self) -> None:
        """
        测试 seaborn_boxplot3 方法。
        
        测试绘制水平箱线图的功能。
        """
        self.assertIsNotNone(self._hello_data)
        
        try:
            fig = self._hello_data.seaborn_boxplot3()
            self.assertIsNotNone(fig)
        except Exception as e:
            self.fail(f"seaborn_boxplot3 执行失败: {e}")

    def test_seaborn_pointplot(self) -> None:
        """
        测试 seaborn_pointplot 方法。
        
        测试绘制点图的功能。
        """
        self.assertIsNotNone(self._hello_data)
        
        try:
            fig = self._hello_data.seaborn_pointplot()
            self.assertIsNotNone(fig)
        except Exception as e:
            self.fail(f"seaborn_pointplot 执行失败: {e}")
        
    def test_seaborn_stripplot(self) -> None:
        """
        测试 seaborn_stripplot 方法。
        
        测试绘制散点图的功能。
        """
        self.assertIsNotNone(self._hello_data)
        
        try:
            fig = self._hello_data.seaborn_stripplot()
            self.assertIsNotNone(fig)
        except Exception as e:
            self.fail(f"seaborn_stripplot 执行失败: {e}")       
        
    def test_df_pivot_table(self) -> None:
        """
        测试 df_pivot_table 方法。
        
        测试使用透视表绘制分组折线图的功能。
        """
        self.assertIsNotNone(self._hello_data)
        
        try:
            fig = self._hello_data.df_pivot_table()
            self.assertIsNotNone(fig)
        except Exception as e:
            self.fail(f"df_pivot_table 执行失败: {e}")
    
    def test_dataframe_property(self) -> None:
        """
        测试 dataframe 属性。
        
        验证 dataframe 属性返回正确的数据。
        """
        self.assertIsNotNone(self._hello_data)
        self.assertIsNotNone(self._hello_data.dataframe)
        self.assertFalse(self._hello_data.dataframe.empty)


if __name__ == '__main__':
    unittest.main(verbosity=2)
