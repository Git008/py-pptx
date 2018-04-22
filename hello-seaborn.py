# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:16:11 2018

@author: Administrator
"""
# 数据分析
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 箱线图
def hello_seaborn_boxplot(excel_data, sheet_name):
    # 导入数据集
    df = pd.read_excel(excel_data, sheet_name)

    # 方法1
    print('Seaborn boxplot 1....')
    sns.boxplot(x='Project', y='Lead Time', data=df)
    plt.show()
    
    # 方法2
    print('Seaborn boxplot 2....')
    sns.boxplot(x=df['Project'], y=df['Lead Time'])
    plt.show()
    
    # 方法3：横的箱线图
    print('Seaborn boxplot 3....')
    sns.boxplot(x=df['Lead Time'], y=df['Project'], orient='h')
    plt.show()
  
def hello_seaborn_pointplot(excel_data, sheet_name):
    # 导入数据集
    df = pd.read_excel(excel_data, sheet_name)
    sns.pointplot(x='Story Finsh Date', y='Lead Time', data=df)
    plt.show()

# 分组折线图
def hello_pivot_table(excel_data, sheet_name):
    # 导入数据集
    df = pd.read_excel(excel_data, sheet_name)

    df.pivot_table(index=['Story Finish Date'], columns='Project', values='Lead Time') \
      .plot(title='Lead Time', style='-o')
    plt.show()
    
# 散点图
def hello_seaborn_stripplot(excel_data, sheet_name):
    # 导入数据集
    df = pd.read_excel(excel_data, sheet_name)
    sns.stripplot(x='Story Finish Date', y='Lead Time', data=df, hue='Project')
    plt.show()

# 测试
hello_seaborn_boxplot('./resource/data0.xlsx', 'Sheet1')    
hello_pivot_table('./resource/data0.xlsx', 'Sheet1')