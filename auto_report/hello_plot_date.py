# -*- coding: utf-8 -*-
"""
Created on Sun May 27 21:31:46 2018

@author: Administrator
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.pylab import date2num

# 读取数据
df = pd.read_excel('../resources/data/data0.xlsx', 'Sheet1')

df['Story开始时间'] = pd.to_datetime(df['Story开始时间'], format='%Y/%m/%d')
df['Story完成时间'] = pd.to_datetime(df['Story完成时间'], format='%Y/%m/%d')
df = df.set_index('Story开始时间')

# 删除Story完成时间为空的行
df.dropna(subset=['Story完成时间'], how='all', inplace=True)

#添加一列，用例汇总计数
df['Total'] = 1

#按天统计
daily = df.resample('D').sum()

#日期序列图
plt.plot_date(daily.index, daily['Total'], fmt='b.')

#坐标
ax = plt.gca()

#设置x轴日期显示格式
ax.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))

#设置x轴日期间隔
autodates = AutoDateLocator()
ax.xaxis.set_major_locator(autodates)

#日期自动旋转
plt.gcf().autofmt_xdate()

#显示图形
plt.show()

