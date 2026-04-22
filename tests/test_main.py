# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 21:38:43 2018

@author: Administrator
"""
from __future__ import annotations

import os
import sys
from typing import List, Type

import unittest


def add_project_root_to_path() -> None:
    """
    将项目根目录添加到 Python 路径中。
    
    确保测试文件可以正确导入 auto_report 模块。
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


def create_test_suite(
    test_classes: List[Type[unittest.TestCase]]
) -> unittest.TestSuite:
    """
    创建测试套件。
    
    Args:
        test_classes: 要包含在测试套件中的测试类列表
        
    Returns:
        unittest.TestSuite: 包含所有测试的测试套件
    """
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_tests(verbosity: int = 2) -> unittest.TestResult:
    """
    运行所有测试。
    
    Args:
        verbosity: 测试输出的详细程度（0、1 或 2）
        
    Returns:
        unittest.TestResult: 测试结果对象
    """
    add_project_root_to_path()
    
    from test_hello_data import TestHelloData
    from test_hello_selenium import TestHelloSelenium
    from test_hello_pptx import TestHelloPptx
    
    test_classes = [
        TestHelloPptx,
        TestHelloData,
        TestHelloSelenium,
    ]
    
    suite = create_test_suite(test_classes)
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result


def print_test_summary(result: unittest.TestResult) -> None:
    """
    打印测试摘要。
    
    Args:
        result: 测试结果对象
    """
    print("\n" + "=" * 60)
    print("测试摘要")
    print("=" * 60)
    print(f"运行测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n出错的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if result.skipped:
        print("\n跳过的测试:")
        for test, reason in result.skipped:
            print(f"  - {test}: {reason}")
    
    print("=" * 60)


if __name__ == '__main__':
    try:
        result = run_tests(verbosity=2)
        print_test_summary(result)
        
        sys.exit(0 if result.wasSuccessful() else 1)
        
    except Exception as e:
        print(f"运行测试时发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
