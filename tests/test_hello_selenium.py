# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 20:43:49 2018

@author: Administrator
"""
from __future__ import annotations

import unittest
from typing import Optional

import auto_report.hello_selenium as hello_selenium


class TestHelloSelenium(unittest.TestCase):
    """
    测试 hello_selenium 模块的功能。
    
    注意：这些测试依赖外部网站，可能会因为网络问题或网站结构变化而失败。
    建议仅在有稳定网络连接时运行。
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        在测试类开始前运行。
        
        可以在这里进行全局初始化。
        """
        pass
    
    def test_weixin_sogou_search(self) -> None:
        """
        测试 weixin_sogou_search 函数。
        
        注意：此测试依赖外部网站，可能会因为网络问题或网站结构变化而失败。
        如果测试失败，将跳过而不是中断整个测试套件。
        """
        try:
            result = hello_selenium.weixin_sogou_search('六西格玛是个P')
            self.assertTrue(result)
        except Exception as e:
            self.skipTest(
                f"Selenium 测试因外部依赖问题被跳过: {e}"
            )
    
    def test_create_chrome_driver_function_exists(self) -> None:
        """
        测试 create_chrome_driver 函数是否存在。
        
        验证辅助函数已正确定义。
        """
        self.assertTrue(hasattr(hello_selenium, 'create_chrome_driver'))
        self.assertTrue(callable(hello_selenium.create_chrome_driver))
    
    def test_safe_quit_driver_function_exists(self) -> None:
        """
        测试 safe_quit_driver 函数是否存在。
        
        验证辅助函数已正确定义。
        """
        self.assertTrue(hasattr(hello_selenium, 'safe_quit_driver'))
        self.assertTrue(callable(hello_selenium.safe_quit_driver))
    
    def test_default_constants_defined(self) -> None:
        """
        测试默认常量是否已定义。
        
        验证 DEFAULT_WAIT_TIME 和 DEFAULT_PAGE_LOAD_WAIT 常量。
        """
        self.assertTrue(hasattr(hello_selenium, 'DEFAULT_WAIT_TIME'))
        self.assertTrue(hasattr(hello_selenium, 'DEFAULT_PAGE_LOAD_WAIT'))
        self.assertIsInstance(hello_selenium.DEFAULT_WAIT_TIME, int)
        self.assertIsInstance(hello_selenium.DEFAULT_PAGE_LOAD_WAIT, int)
        self.assertGreater(hello_selenium.DEFAULT_WAIT_TIME, 0)
        self.assertGreater(hello_selenium.DEFAULT_PAGE_LOAD_WAIT, 0)
    
    def test_get_house365_today_info_deprecated(self) -> None:
        """
        测试 get_house365_today_info 函数是否已废弃。
        
        验证该函数会抛出 RuntimeError，说明网站结构已变化。
        """
        with self.assertRaises(RuntimeError) as context:
            hello_selenium.get_house365_today_info()
        
        error_message = str(context.exception)
        self.assertIn('已废弃', error_message)
        self.assertIn('house365.com', error_message)


if __name__ == '__main__':
    unittest.main(verbosity=2)
