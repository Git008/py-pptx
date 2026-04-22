# -*- coding: utf-8 -*-
"""
Created on Sun May 27 21:31:46 2018

@author: Administrator
"""
from __future__ import annotations

import os
from typing import Optional, Union, TYPE_CHECKING

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import AutoDateLocator, DateFormatter

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(PROJECT_ROOT, 'resources')
DATA_DIR = os.path.join(RESOURCES_DIR, 'data')


def load_and_process_data(
    data_path: Optional[Union[str, os.PathLike]] = None
) -> pd.DataFrame:
    """
    加载并处理 Excel 数据文件。
    
    读取 Excel 文件，转换日期列，设置索引，删除空值，并添加统计列。
    
    Args:
        data_path: Excel 数据文件路径。如果为 None，则使用默认路径
        
    Returns:
        pd.DataFrame: 处理后的数据框，按天重采样的统计结果
        
    Raises:
        FileNotFoundError: 如果数据文件不存在
        ValueError: 如果数据格式不正确或缺少必要的列
        ImportError: 如果缺少必要的依赖
    """
    if data_path is None:
        data_path = os.path.join(DATA_DIR, 'data0.xlsx')
    
    try:
        data_path_str = os.fspath(data_path)
        
        if not os.path.exists(data_path_str):
            raise FileNotFoundError(f"数据文件不存在: {data_path_str}")
        
        df = pd.read_excel(data_path_str, sheet_name='Sheet1')
        
        if df.empty:
            raise ValueError("Excel 文件中没有数据")
        
        required_columns = ['Story开始时间', 'Story完成时间']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"数据缺少必要的列: {', '.join(missing_cols)}")
        
        df['Story开始时间'] = pd.to_datetime(df['Story开始时间'], format='%Y/%m/%d')
        df['Story完成时间'] = pd.to_datetime(df['Story完成时间'], format='%Y/%m/%d')
        df = df.set_index('Story开始时间')
        
        df.dropna(subset=['Story完成时间'], how='all', inplace=True)
        
        df['Total'] = 1
        
        daily = df.resample('D').sum()
        
        return daily
        
    except FileNotFoundError:
        raise
    except ValueError:
        raise
    except ImportError as ie:
        if "openpyxl" in str(ie):
            raise ImportError(
                "缺少 openpyxl 依赖，请运行: pip install openpyxl>=3.1.5"
            ) from ie
        raise
    except Exception as e:
        raise RuntimeError(f"加载和处理数据时出错: {e}") from e


def create_date_series_plot(
    daily_data: pd.DataFrame,
    show_plot: bool = True
) -> Figure:
    """
    创建日期序列图。
    
    根据按天统计的数据绘制日期序列图，显示每天的数量变化。
    
    Args:
        daily_data: 按天重采样的统计数据框
        show_plot: 是否显示图形
        
    Returns:
        matplotlib.figure.Figure: 生成的图表对象
        
    Raises:
        ValueError: 如果数据格式不正确
        KeyError: 如果数据缺少必要的列
    """
    if daily_data.empty:
        raise ValueError("数据为空，无法绘制图表")
    
    if 'Total' not in daily_data.columns:
        raise KeyError("数据缺少 'Total' 列")
    
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot_date(daily_data.index, daily_data['Total'], fmt='b.')
        
        ax.set_title('每日数据统计')
        ax.set_xlabel('日期')
        ax.set_ylabel('数量')
        ax.grid(True, alpha=0.3)
        
        ax.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
        autodates = AutoDateLocator()
        ax.xaxis.set_major_locator(autodates)
        
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return fig
        
    except KeyError:
        plt.close('all')
        raise
    except ValueError:
        plt.close('all')
        raise
    except Exception as e:
        plt.close('all')
        raise RuntimeError(f"绘制日期序列图时出错: {e}") from e
    finally:
        if not show_plot:
            plt.close('all')


def run_date_series_analysis(
    data_path: Optional[Union[str, os.PathLike]] = None,
    show_plot: bool = True
) -> tuple[pd.DataFrame, Figure]:
    """
    运行完整的日期序列分析流程。
    
    加载数据、处理数据并绘制日期序列图的一站式函数。
    
    Args:
        data_path: Excel 数据文件路径。如果为 None，则使用默认路径
        show_plot: 是否显示图形
        
    Returns:
        tuple[pd.DataFrame, Figure]: 包含 (处理后的数据, 图表对象) 的元组
        
    Raises:
        FileNotFoundError: 如果数据文件不存在
        ValueError: 如果数据格式不正确
        RuntimeError: 如果分析过程中出错
    """
    try:
        daily_data = load_and_process_data(data_path)
        
        fig = create_date_series_plot(daily_data, show_plot=show_plot)
        
        return daily_data, fig
        
    except FileNotFoundError:
        raise
    except ValueError:
        raise
    except Exception as e:
        plt.close('all')
        raise RuntimeError(f"日期序列分析失败: {e}") from e


if __name__ == '__main__':
    try:
        daily_data, fig = run_date_series_analysis(show_plot=True)
        
        print(f"日期序列分析完成")
        print(f"数据范围: {daily_data.index.min().date()} 至 {daily_data.index.max().date()}")
        print(f"总天数: {len(daily_data)}")
        print(f"总数量: {daily_data['Total'].sum()}")
        
    except FileNotFoundError as e:
        print(f"错误: {e}")
    except ValueError as e:
        print(f"数据错误: {e}")
    except RuntimeError as e:
        print(f"运行时错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
