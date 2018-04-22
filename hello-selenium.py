# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:09:04 2018

@author: Administrator
"""

# web 
from selenium import webdriver

# excel
import xlwt
import time

def hello_selenium():
    # chromedriverv2.3.7 配套chromev65
    browser = webdriver.Chrome('./driver/chromedriver2.3.7.exe')
    
    # 打开指定网页
    url = "http://weixin.sogou.com/"  
    browser.get(url)
    
    # 在微信搜索框中输入关键字"六西格玛是个P"，通过ID查找
    browser.find_element_by_id('query').send_keys('六西格玛是个P')
    # 单击公众号搜索按钮，通过class查找
    browser.find_element_by_class_name('swz2').click()
    
    # 关闭浏览器
    time.sleep(3)  
    browser.quit()
    
def hello_table_data():
    # chromedriverv2.3.7 配套chromev65
    browser = webdriver.Chrome('./driver/chromedriver2.3.7.exe')
    
    # 打开指定网
    browser.get('http://newhouse.nj.house365.com/')
    
    # 等待5秒，页面加载OK，解决NoSuchElementException问题
    time.sleep(5)    
    
    #创建工作簿  
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)  
    #创建工作表  
    sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)  
 
    #今日交易信息快递
    #将表的每一行存在table_tr_list中
    table_body_xpath = '/html/body/div[19]/div[2]/div[2]/div[1]/table/tbody'
    table_body = browser.find_element_by_xpath(table_body_xpath)
    table_tr_list = table_body.find_elements_by_tag_name('tr')  
    
    # 从excel第一行开始存
    for r,tr in enumerate(table_tr_list, 0):  
        #将表的每一行的每一列内容存在table_td_list中  
        table_td_list = tr.find_elements_by_tag_name('td')  
        #写入表的内容到sheet 1中，第r行第c列  
        for c,td in enumerate(table_td_list):  
            sheet.write(r, c, td.text) 
            
    #保存表格到已有的 excel  
    wbk.save('test.xls')   
    
    # 关闭浏览器
    time.sleep(3) 
    browser.quit() 