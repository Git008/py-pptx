# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 20:54:18 2018

@author: Administrator
"""
from __future__ import annotations

import os
from typing import List, Dict, Optional, TYPE_CHECKING

import unittest

from pptx import Presentation
from pptx.presentation import Presentation as PresentationType

import auto_report.hello_pptx as hello_pptx

if TYPE_CHECKING:
    from pptx.slide import Slide

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(PROJECT_ROOT, 'resources')
TEMPLATE_DIR = os.path.join(RESOURCES_DIR, 'template')
REPORT_DIR = os.path.join(RESOURCES_DIR, 'report')


class TestHelloPptx(unittest.TestCase):
    """
    测试 hello_pptx 模块的功能。
    
    测试 PPT 操作，包括添加幻灯片布局、添加文本、创建图表幻灯片等。
    """
    
    _template_path: str = ""
    _prs: Optional[PresentationType] = None
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        在测试类开始前初始化测试数据。
        """
        cls._template_path = os.path.join(TEMPLATE_DIR, 'ppt_template0.pptx')
        
        if not os.path.exists(cls._template_path):
            raise FileNotFoundError(f"PPT 模板文件不存在: {cls._template_path}")
        
        os.makedirs(REPORT_DIR, exist_ok=True)
    
    def setUp(self) -> None:
        """
        在每个测试方法开始前运行。
        
        创建新的 Presentation 实例。
        """
        self._prs = Presentation(self._template_path)
    
    def tearDown(self) -> None:
        """
        在每个测试方法结束后运行。
        
        清理资源。
        """
        self._prs = None
    
    def test_add_all_slide_layout(self) -> None:
        """
        测试 add_all_slide_layout 函数。
        
        测试为演示文稿添加所有类型的幻灯片布局。
        """
        self.assertIsNotNone(self._prs)
        
        try:
            initial_slide_count = len(self._prs.slides)
            
            new_slides = hello_pptx.add_all_slide_layout(self._prs)
            
            self.assertIsInstance(new_slides, list)
            self.assertGreater(len(new_slides), 0)
            self.assertEqual(len(self._prs.slides), initial_slide_count + len(new_slides))
            
            output_path = os.path.join(REPORT_DIR, 'slide_layout.pptx')
            self._prs.save(output_path)
            
            self.assertTrue(os.path.exists(output_path))
            
        except Exception as e:
            self.fail(f"add_all_slide_layout 执行失败: {e}")
    
    def test_add_shape_text(self) -> None:
        """
        测试 add_text_by_shape 和 add_text_by_palceholder 函数。
        
        测试通过形状和占位符添加文本的功能。
        """
        self.assertIsNotNone(self._prs)
        
        try:
            slide_layout = self._prs.slide_layouts[4]
            
            slide1: Slide = self._prs.slides.add_slide(slide_layout)
            result1 = hello_pptx.add_text_by_shape(slide1)
            self.assertIsInstance(result1, dict)
            
            slide2: Slide = self._prs.slides.add_slide(slide_layout)
            result2 = hello_pptx.add_text_by_palceholder(slide2)
            self.assertIsInstance(result2, dict)
            
            output_path = os.path.join(REPORT_DIR, 'add_shape_text.pptx')
            self._prs.save(output_path)
            
            self.assertTrue(os.path.exists(output_path))
            
        except Exception as e:
            self.fail(f"add_shape_text 测试失败: {e}")
    
    def test_ensure_report_dir(self) -> None:
        """
        测试 ensure_report_dir 函数。
        
        测试确保报告目录存在的功能。
        """
        try:
            result = hello_pptx.ensure_report_dir()
            self.assertEqual(os.path.normcase(result), os.path.normcase(REPORT_DIR))
            self.assertTrue(os.path.exists(result))
            self.assertTrue(os.path.isdir(result))
        except Exception as e:
            self.fail(f"ensure_report_dir 执行失败: {e}")
    
    def test_slide_layout_names_constant(self) -> None:
        """
        测试 SLIDE_LAYOUT_NAMES 常量。
        
        验证常量定义正确。
        """
        self.assertIsInstance(hello_pptx.SLIDE_LAYOUT_NAMES, dict)
        self.assertGreater(len(hello_pptx.SLIDE_LAYOUT_NAMES), 0)
        
        for key, value in hello_pptx.SLIDE_LAYOUT_NAMES.items():
            self.assertIsInstance(key, int)
            self.assertIsInstance(value, str)
            self.assertGreater(len(value), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
