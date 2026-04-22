# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:16:11 2018

@author: Administrator
"""
from __future__ import annotations

import os
from typing import Optional, Union, Any, TYPE_CHECKING

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

if TYPE_CHECKING:
    from pathlib import Path
    from matplotlib.figure import Figure


class HelloData:
    """
    数据分析和可视化类，用于处理数据并生成各种图表。
    
    Attributes:
        _df: pandas DataFrame，存储加载的数据
    """
    
    def __init__(self, wbk: Union[str, os.PathLike], sheet: str) -> None:
        """
        初始化 HelloData 类，从 Excel 文件加载数据。
        
        Args:
            wbk: Excel 文件路径
            sheet: 工作表名称
        
        Raises:
            FileNotFoundError: 如果文件不存在
            ValueError: 如果工作表不存在或数据格式错误
            ImportError: 如果缺少必要的依赖（如 openpyxl）
        """
        self._df: Optional[pd.DataFrame] = None
        
        try:
            if not os.path.exists(wbk):
                raise FileNotFoundError(f"Excel 文件不存在: {wbk}")
            
            self._df = pd.read_excel(wbk, sheet_name=sheet)
            
            if self._df.empty:
                raise ValueError(f"工作表 '{sheet}' 中没有数据")
                
        except FileNotFoundError:
            raise
        except ValueError as ve:
            if "Worksheet named" in str(ve) and "not found" in str(ve):
                raise ValueError(f"工作表 '{sheet}' 不存在于文件中") from ve
            raise
        except ImportError as ie:
            if "openpyxl" in str(ie):
                raise ImportError(
                    "缺少 openpyxl 依赖，请运行: pip install openpyxl>=3.1.5"
                ) from ie
            raise
        except Exception as e:
            raise RuntimeError(f"加载 Excel 文件时出错: {e}") from e
    
    @property
    def dataframe(self) -> Optional[pd.DataFrame]:
        """获取加载的数据 DataFrame。"""
        return self._df
    
    def _validate_data(self) -> None:
        """
        验证数据是否已加载。
        
        Raises:
            ValueError: 如果数据未加载
        """
        if self._df is None or self._df.empty:
            raise ValueError("数据未加载或为空，请先加载有效的数据文件")
    
    def seaborn_boxplot1(self) -> Figure:
        """
        使用 seaborn 绘制箱线图（方法1：使用列名）。
        
        按 'Project' 分组显示 'Lead Time' 的分布。
        
        Returns:
            matplotlib.figure.Figure: 生成的图表对象
        
        Raises:
            ValueError: 如果数据未加载或缺少必要的列
        """
        self._validate_data()
        
        required_columns = ['Project', 'Lead Time']
        missing_cols = [col for col in required_columns if col not in self._df.columns]
        if missing_cols:
            raise ValueError(f"数据缺少必要的列: {', '.join(missing_cols)}")
        
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x='Project', y='Lead Time', data=self._df, ax=ax)
            ax.set_title('Lead Time 箱线图（按 Project 分组）')
            ax.set_xlabel('项目')
            ax.set_ylabel('交付周期')
            plt.tight_layout()
            plt.show()
            return fig
        except Exception as e:
            plt.close('all')
            raise RuntimeError(f"绘制箱线图时出错: {e}") from e
        finally:
            plt.close('all')

    def seaborn_boxplot2(self) -> Figure:
        """
        使用 seaborn 绘制箱线图（方法2：直接传递 Series）。
        
        按 'Project' 分组显示 'Lead Time' 的分布。
        
        Returns:
            matplotlib.figure.Figure: 生成的图表对象
        
        Raises:
            ValueError: 如果数据未加载或缺少必要的列
        """
        self._validate_data()
        
        required_columns = ['Project', 'Lead Time']
        missing_cols = [col for col in required_columns if col not in self._df.columns]
        if missing_cols:
            raise ValueError(f"数据缺少必要的列: {', '.join(missing_cols)}")
        
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x=self._df['Project'], y=self._df['Lead Time'], ax=ax)
            ax.set_title('Lead Time 箱线图（按 Project 分组）')
            ax.set_xlabel('项目')
            ax.set_ylabel('交付周期')
            plt.tight_layout()
            plt.show()
            return fig
        except Exception as e:
            plt.close('all')
            raise RuntimeError(f"绘制箱线图时出错: {e}") from e
        finally:
            plt.close('all')
        
    def seaborn_boxplot3(self) -> Figure:
        """
        使用 seaborn 绘制水平箱线图。
        
        水平显示 'Lead Time' 按 'Project' 分组的分布。
        
        Returns:
            matplotlib.figure.Figure: 生成的图表对象
        
        Raises:
            ValueError: 如果数据未加载或缺少必要的列
        """
        self._validate_data()
        
        required_columns = ['Project', 'Lead Time']
        missing_cols = [col for col in required_columns if col not in self._df.columns]
        if missing_cols:
            raise ValueError(f"数据缺少必要的列: {', '.join(missing_cols)}")
        
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(
                x=self._df['Lead Time'], 
                y=self._df['Project'], 
                orient='h',
                ax=ax
            )
            ax.set_title('Lead Time 水平箱线图')
            ax.set_xlabel('交付周期')
            ax.set_ylabel('项目')
            plt.tight_layout()
            plt.show()
            return fig
        except Exception as e:
            plt.close('all')
            raise RuntimeError(f"绘制水平箱线图时出错: {e}") from e
        finally:
            plt.close('all')
    
    def seaborn_pointplot(self) -> Figure:
        """
        使用 seaborn 绘制点图。
        
        显示 'Story完成时间' 与 'Lead Time' 的关系。
        
        Returns:
            matplotlib.figure.Figure: 生成的图表对象
        
        Raises:
            ValueError: 如果数据未加载或缺少必要的列
        """
        self._validate_data()
        
        required_columns = ['Story完成时间', 'Lead Time']
        missing_cols = [col for col in required_columns if col not in self._df.columns]
        if missing_cols:
            raise ValueError(f"数据缺少必要的列: {', '.join(missing_cols)}")
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.pointplot(x='Story完成时间', y='Lead Time', data=self._df, ax=ax)
            ax.set_title('Lead Time 点图（按 Story完成时间）')
            ax.set_xlabel('Story 完成时间')
            ax.set_ylabel('交付周期')
            plt.gcf().autofmt_xdate()
            plt.tight_layout()
            plt.show()
            return fig
        except Exception as e:
            plt.close('all')
            raise RuntimeError(f"绘制点图时出错: {e}") from e
        finally:
            plt.close('all')
        
    def seaborn_stripplot(self) -> Figure:
        """
        使用 seaborn 绘制散点图。
        
        显示 'Story完成时间' 与 'Lead Time' 的关系，按 'Project' 着色。
        
        Returns:
            matplotlib.figure.Figure: 生成的图表对象
        
        Raises:
            ValueError: 如果数据未加载或缺少必要的列
        """
        self._validate_data()
        
        required_columns = ['Story完成时间', 'Lead Time', 'Project']
        missing_cols = [col for col in required_columns if col not in self._df.columns]
        if missing_cols:
            raise ValueError(f"数据缺少必要的列: {', '.join(missing_cols)}")
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.stripplot(
                x='Story完成时间', 
                y='Lead Time', 
                data=self._df, 
                hue='Project',
                ax=ax
            )
            
            ax.set_title('Lead Time 散点图（按 Project 着色）')
            ax.set_xlabel('Story 完成时间')
            ax.set_ylabel('交付周期')
            
            plt.gcf().autofmt_xdate()
            plt.legend(bbox_to_anchor=(1.02, 1.0), borderaxespad=0, loc='upper left')
            plt.tight_layout()
            plt.subplots_adjust(right=0.8)
            plt.show()
            return fig
        except Exception as e:
            plt.close('all')
            raise RuntimeError(f"绘制散点图时出错: {e}") from e
        finally:
            plt.close('all')
    
    def df_pivot_table(self) -> Figure:
        """
        使用 pandas 透视表绘制分组折线图。
        
        显示不同项目的 'Lead Time' 随 'Story完成时间' 的变化趋势。
        
        Returns:
            matplotlib.figure.Figure: 生成的图表对象
        
        Raises:
            ValueError: 如果数据未加载或缺少必要的列
        """
        self._validate_data()
        
        required_columns = ['Story完成时间', 'Lead Time', 'Project']
        missing_cols = [col for col in required_columns if col not in self._df.columns]
        if missing_cols:
            raise ValueError(f"数据缺少必要的列: {', '.join(missing_cols)}")
        
        try:
            pivot = self._df.pivot_table(
                index=['Story完成时间'], 
                columns='Project', 
                values='Lead Time'
            )
            
            ax = pivot.plot(title='Lead Time 趋势图', style='-o', figsize=(12, 6))
            ax.set_xlabel('Story 完成时间')
            ax.set_ylabel('交付周期')
            
            plt.legend(bbox_to_anchor=(1.02, 1.0), borderaxespad=0, loc='upper left')
            plt.gcf().autofmt_xdate()
            plt.tight_layout()
            plt.subplots_adjust(right=0.8)
            plt.show()
            
            return ax.figure
        except Exception as e:
            plt.close('all')
            raise RuntimeError(f"绘制分组折线图时出错: {e}") from e
        finally:
            plt.close('all')
