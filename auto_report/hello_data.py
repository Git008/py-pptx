# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:16:11 2018

@author: Administrator
"""
# 数据分析
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

import time
from datetime import datetime

class HelloData():
    _df = None
    
    def __init__(self, wbk, sheet):
        # 导入数据集
        self._df = pd.read_excel(wbk, sheet)
    
    # 箱线图方法1
    def seaborn_boxplot1(self):
        sns.boxplot(x='Project', y='Lead Time', data=self._df)
        plt.show()

    # 箱线图方法2
    def seaborn_boxplot2(self):
        sns.boxplot(x=self._df['Project'], y=self._df['Lead Time'])
        plt.show()
        
    # 箱线图方法3
    def seaborn_boxplot3(self):
        sns.boxplot(x=self._df['Lead Time'], y=self._df['Project'], orient='h')
        plt.show()
    
    # 散点图
    def seaborn_pointplot(self):
        self._df['Story完成时间'] = pd.to_datetime(self._df['Story完成时间'], format='%Y/%m%d')
        
        sns.pointplot(x='Story完成时间', y='Lead Time', data=self._df)
        plt.show()
        
    # 散点图
    # 待解决问题：ValueError: Could not interpret input 'Story Finsh Date'
    def seaborn_stripplot(self):
        sns.stripplot(x='Story完成时间', y='Lead Time', data=self._df, hue='Project')
        plt.show()
    
    # 分组折线图
    def df_pivot_table(self):
        self._df['Story完成时间'] = pd.to_datetime(self._df['Story完成时间'], format='%Y/%m/%d')
        
        self._df.pivot_table(index=['Story完成时间'], columns='Project', values='Lead Time') \
            .plot(title='Lead Time', style='-o')
        plt.show()