# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:09:04 2018

@author: Administrator
"""
from __future__ import annotations

import os
import time
from typing import Optional, List, Dict, Any, TYPE_CHECKING, Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    TimeoutException,
    SessionNotCreatedException
)
from webdriver_manager.chrome import ChromeDriverManager

import xlwt

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.chrome.webdriver import WebDriver

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(PROJECT_ROOT, 'resources')
DATA_DIR = os.path.join(RESOURCES_DIR, 'data')
REPORT_DIR = os.path.join(RESOURCES_DIR, 'report')
TEMPLATE_DIR = os.path.join(RESOURCES_DIR, 'template')
DRIVER_DIR = os.path.join(RESOURCES_DIR, 'driver')

DEFAULT_WAIT_TIME: int = 3
DEFAULT_PAGE_LOAD_WAIT: int = 10


def create_chrome_driver(
    headless: bool = True,
    additional_options: Optional[List[str]] = None
) -> WebDriver:
    """
    创建 Chrome 浏览器驱动实例。
    
    使用 webdriver_manager 自动管理 ChromeDriver 版本，
    并配置常用的浏览器选项。
    
    Args:
        headless: 是否使用无头模式（不显示浏览器窗口）
        additional_options: 额外的 Chrome 选项列表
        
    Returns:
        WebDriver: Chrome 浏览器驱动实例
        
    Raises:
        SessionNotCreatedException: 如果无法创建浏览器会话
        WebDriverException: 如果初始化浏览器驱动时出错
        RuntimeError: 如果安装或配置 ChromeDriver 时出错
    """
    try:
        service = Service(ChromeDriverManager().install())
        
        options = ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        if additional_options:
            for opt in additional_options:
                options.add_argument(opt)
        
        driver = webdriver.Chrome(service=service, options=options)
        return driver
        
    except SessionNotCreatedException as e:
        raise SessionNotCreatedException(
            f"无法创建 Chrome 浏览器会话。请确保 Chrome 浏览器已安装: {e}"
        ) from e
    except WebDriverException as e:
        raise WebDriverException(
            f"初始化 Chrome 驱动时出错: {e}"
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"创建浏览器驱动时发生未知错误: {e}"
        ) from e


def safe_quit_driver(driver: Optional[WebDriver]) -> None:
    """
    安全地关闭浏览器驱动，忽略任何异常。
    
    Args:
        driver: 浏览器驱动实例，可以为 None
    """
    if driver is not None:
        try:
            driver.quit()
        except Exception:
            pass


def weixin_sogou_search(weixin_name: str, wait_time: int = DEFAULT_WAIT_TIME) -> bool:
    """
    在搜狗微信搜索中搜索公众号。
    
    注意：此函数依赖外部网站的结构，可能会因为网站改版而失效。
    建议仅用于演示和学习目的。
    
    Args:
        weixin_name: 要搜索的公众号名称
        wait_time: 操作后的等待时间（秒）
        
    Returns:
        bool: 如果搜索操作成功完成返回 True，否则返回 False
        
    Raises:
        ValueError: 如果 weixin_name 为空
        WebDriverException: 如果浏览器操作出错
    """
    if not weixin_name or not weixin_name.strip():
        raise ValueError("公众号名称不能为空")
    
    driver: Optional[WebDriver] = None
    
    try:
        driver = create_chrome_driver(headless=True)
        
        url = "http://weixin.sogou.com/"
        driver.get(url)
        
        time.sleep(wait_time)
        
        search_input = driver.find_element(By.ID, 'query')
        search_input.send_keys(weixin_name)
        
        search_button = driver.find_element(By.CLASS_NAME, 'swz2')
        search_button.click()
        
        time.sleep(wait_time)
        
        return True
        
    except NoSuchElementException as e:
        raise RuntimeError(
            f"无法找到页面元素，网站结构可能已变化: {e}"
        ) from e
    except TimeoutException as e:
        raise RuntimeError(
            f"页面加载超时: {e}"
        ) from e
    except WebDriverException as e:
        raise WebDriverException(
            f"浏览器操作出错: {e}"
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"执行搜索时发生未知错误: {e}"
        ) from e
    finally:
        safe_quit_driver(driver)


def get_house365_today_info(
    output_path: Optional[Union[str, os.PathLike]] = None,
    page_load_wait: int = DEFAULT_PAGE_LOAD_WAIT
) -> str:
    """
    从 House365 网站获取今日交易信息并保存到 Excel。
    
    注意：此函数依赖外部网站的结构，且代码注释已注明"页面变化，代码暂时不可用"。
    网站结构可能已发生变化，此函数可能无法正常工作。
    
    Args:
        output_path: 输出 Excel 文件的路径。如果为 None，则使用默认路径
        page_load_wait: 页面加载等待时间（秒）
        
    Returns:
        str: 保存的 Excel 文件的绝对路径
        
    Raises:
        RuntimeError: 因为网站结构已变化，此函数已废弃
        NoSuchElementException: 如果无法找到页面元素
        WebDriverException: 如果浏览器操作出错
        OSError: 如果无法保存 Excel 文件
    """
    raise RuntimeError(
        "此函数已废弃，因为目标网站 (house365.com) 的页面结构已发生变化。"
        "原有的 XPath 选择器 '/html/body/div[19]/div[2]/div[2]/div[1]/table/tbody' "
        "已不再适用。请更新代码以适配新的网站结构。"
    )
    
    driver: Optional[WebDriver] = None
    
    try:
        if output_path is None:
            output_path = os.path.join(DATA_DIR, 'house365_today_info.xls')
        
        driver = create_chrome_driver(headless=True)
        
        driver.get('http://newhouse.nj.house365.com/')
        time.sleep(page_load_wait)
        
        wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
        
        table_body_xpath = '/html/body/div[19]/div[2]/div[2]/div[1]/table/tbody'
        table_body: WebElement = driver.find_element(By.XPATH, table_body_xpath)
        table_tr_list: List[WebElement] = table_body.find_elements(By.TAG_NAME, 'tr')
        
        for r, tr in enumerate(table_tr_list, 0):
            table_td_list: List[WebElement] = tr.find_elements(By.TAG_NAME, 'td')
            for c, td in enumerate(table_td_list):
                sheet.write(r, c, td.text)
        
        output_path_str = os.fspath(output_path)
        wbk.save(output_path_str)
        
        return os.path.abspath(output_path_str)
        
    except NoSuchElementException as e:
        raise RuntimeError(
            f"无法找到页面元素，网站结构可能已变化: {e}"
        ) from e
    except TimeoutException as e:
        raise RuntimeError(
            f"页面加载超时: {e}"
        ) from e
    except WebDriverException as e:
        raise WebDriverException(
            f"浏览器操作出错: {e}"
        ) from e
    except OSError as e:
        raise OSError(
            f"保存 Excel 文件时出错: {e}"
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"获取房产信息时发生未知错误: {e}"
        ) from e
    finally:
        safe_quit_driver(driver)
