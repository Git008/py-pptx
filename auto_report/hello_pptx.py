# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 12:12:34 2018

@author: Administrator
"""
from __future__ import annotations

import os
from typing import List, Optional, Dict, Any, TYPE_CHECKING, Union

import matplotlib.pyplot as plt
import pandas as pd

from pptx.util import Inches
from pptx.presentation import Presentation

if TYPE_CHECKING:
    from pptx.slide import Slide, SlideLayout
    from matplotlib.figure import Figure

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(PROJECT_ROOT, 'resources')
DATA_DIR = os.path.join(RESOURCES_DIR, 'data')
REPORT_DIR = os.path.join(RESOURCES_DIR, 'report')
TEMPLATE_DIR = os.path.join(RESOURCES_DIR, 'template')
DRIVER_DIR = os.path.join(RESOURCES_DIR, 'driver')

SLIDE_LAYOUT_NAMES: Dict[int, str] = {
    0: 'Title (presentation title slide)',
    1: 'Title and Content',
    2: 'Section Header (sometimes called Segue)',
    3: 'Two Content (side by side bullet textboxes)',
    4: 'Comparison (same but additional title for each side by side content box)',
    5: 'Title Only',
    6: 'Blank',
    7: 'Content with Caption',
    8: 'Picture with Caption'
}


def ensure_report_dir() -> str:
    """
    确保报告目录存在，如果不存在则创建。
    
    Returns:
        str: 报告目录的绝对路径
    
    Raises:
        OSError: 如果创建目录失败
    """
    try:
        os.makedirs(REPORT_DIR, exist_ok=True)
        return REPORT_DIR
    except OSError as e:
        raise OSError(f"无法创建报告目录 {REPORT_DIR}: {e}") from e


def add_all_slide_layout(prs: Presentation) -> List[Slide]:
    """
    为演示文稿添加所有类型的幻灯片布局。
    
    遍历所有预设的幻灯片布局类型，为每种布局创建一张新幻灯片，
    并在非空白布局的标题框中显示布局名称。
    
    Args:
        prs: python-pptx Presentation 对象
        
    Returns:
        List[Slide]: 新创建的幻灯片列表
    
    Raises:
        TypeError: 如果 prs 不是有效的 Presentation 对象
        IndexError: 如果幻灯片布局索引超出范围
        ValueError: 如果幻灯片没有标题框
    """
    if not isinstance(prs, Presentation):
        raise TypeError("prs 必须是 python-pptx 的 Presentation 对象")
    
    new_slides: List[Slide] = []
    
    try:
        for index in sorted(SLIDE_LAYOUT_NAMES.keys()):
            if index >= len(prs.slide_layouts):
                raise IndexError(
                    f"幻灯片布局索引 {index} 超出范围。"
                    f"演示文稿只有 {len(prs.slide_layouts)} 个布局"
                )
            
            layout_name = SLIDE_LAYOUT_NAMES[index]
            slide_layout: SlideLayout = prs.slide_layouts[index]
            new_slide: Slide = prs.slides.add_slide(slide_layout)
            
            if index != 6:
                title_shape = new_slide.shapes.title
                if title_shape is not None and hasattr(title_shape, 'text_frame'):
                    title_shape.text = layout_name
                else:
                    raise ValueError(f"布局 {index} ({layout_name}) 没有有效的标题框")
            
            new_slides.append(new_slide)
        
        return new_slides
        
    except IndexError:
        raise
    except Exception as e:
        raise RuntimeError(f"添加幻灯片布局时出错: {e}") from e


def add_text_by_shape(slide: Slide) -> Dict[int, str]:
    """
    通过遍历幻灯片中的所有形状来添加文本。
    
    遍历幻灯片中的所有形状，打印每个形状的 ID 和名称，
    并为具有文本框的形状设置文本内容。
    
    Args:
        slide: python-pptx Slide 对象
        
    Returns:
        Dict[int, str]: 包含形状 ID 和对应文本的字典
    
    Raises:
        TypeError: 如果 slide 不是有效的 Slide 对象
    """
    if not hasattr(slide, 'shapes'):
        raise TypeError("slide 必须是 python-pptx 的 Slide 对象")
    
    result: Dict[int, str] = {}
    
    try:
        for i, shape in enumerate(slide.shapes):
            shape_id = shape.shape_id
            shape_name = shape.name
            
            print(f'{shape_id} {shape_name}')
            
            if shape.has_text_frame:
                text = f'add_text_by_shape {i}'
                shape.text = text
                result[shape_id] = text
        
        return result
        
    except Exception as e:
        raise RuntimeError(f"通过形状添加文本时出错: {e}") from e


def add_text_by_palceholder(slide: Slide) -> Dict[int, str]:
    """
    通过遍历幻灯片中的占位符来添加文本。
    
    遍历幻灯片中的所有占位符，打印每个占位符的索引和名称，
    并为具有文本框的占位符设置文本内容。
    
    Args:
        slide: python-pptx Slide 对象
        
    Returns:
        Dict[int, str]: 包含占位符索引和对应文本的字典
    
    Raises:
        TypeError: 如果 slide 不是有效的 Slide 对象
    """
    if not hasattr(slide, 'placeholders'):
        raise TypeError("slide 必须是 python-pptx 的 Slide 对象")
    
    result: Dict[int, str] = {}
    
    try:
        for i, shape in enumerate(slide.placeholders):
            placeholder_idx = shape.placeholder_format.idx
            shape_name = shape.name
            
            print(f'{placeholder_idx} {shape_name}')
            
            if shape.has_text_frame:
                text = f'add_text_by_palceholder {i}'
                shape.text = text
                result[placeholder_idx] = text
        
        return result
        
    except Exception as e:
        raise RuntimeError(f"通过占位符添加文本时出错: {e}") from e


def page1_boxplot(prs: Presentation, data_path: Optional[Union[str, os.PathLike]] = None) -> Slide:
    """
    在演示文稿中添加一张包含箱线图的幻灯片。
    
    从 Excel 文件加载数据，绘制箱线图并保存为图片，
    然后将图片插入到新创建的幻灯片中。
    
    Args:
        prs: python-pptx Presentation 对象
        data_path: Excel 数据文件路径。如果为 None，则使用默认路径
        
    Returns:
        Slide: 新创建的包含箱线图的幻灯片
    
    Raises:
        TypeError: 如果 prs 不是有效的 Presentation 对象
        FileNotFoundError: 如果数据文件不存在
        ValueError: 如果数据格式不正确或缺少必要的列
        ImportError: 如果缺少必要的依赖（如 openpyxl）
    """
    if not isinstance(prs, Presentation):
        raise TypeError("prs 必须是 python-pptx 的 Presentation 对象")
    
    if data_path is None:
        data_path = os.path.join(DATA_DIR, 'data0.xlsx')
    
    try:
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"数据文件不存在: {data_path}")
        
        if len(prs.slide_layouts) < 2:
            raise ValueError("演示文稿的幻灯片布局数量不足，需要至少 2 个布局")
        
        title_slide_layout: SlideLayout = prs.slide_layouts[1]
        slide: Slide = prs.slides.add_slide(title_slide_layout)
        
        title_shape = slide.shapes.title
        if title_shape is not None and hasattr(title_shape, 'text_frame'):
            title_shape.text = '箱线图示例'
        
        df = pd.read_excel(data_path, sheet_name='Sheet1')
        
        if df.empty:
            raise ValueError("Excel 文件中没有数据")
        
        required_columns = ['Project', 'Lead Time']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"数据缺少必要的列: {', '.join(missing_cols)}")
        
        ensure_report_dir()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        df.boxplot(column='Lead Time', by='Project', ax=ax)
        ax.set_title('Lead Time 箱线图（按 Project 分组）')
        ax.set_xlabel('项目')
        ax.set_ylabel('交付周期')
        plt.suptitle('')
        plt.tight_layout()
        
        img_path = os.path.join(REPORT_DIR, '交付周期_箱线图.png')
        plt.savefig(img_path, dpi=150, bbox_inches='tight')
        plt.close('all')
        
        left = Inches(1)
        top = Inches(1.8)
        width = Inches(4.5)
        height = Inches(4.5)
        slide.shapes.add_picture(img_path, left, top, width, height)
        
        return slide
        
    except FileNotFoundError:
        plt.close('all')
        raise
    except ValueError:
        plt.close('all')
        raise
    except ImportError as ie:
        plt.close('all')
        if "openpyxl" in str(ie):
            raise ImportError(
                "缺少 openpyxl 依赖，请运行: pip install openpyxl>=3.1.5"
            ) from ie
        raise
    except Exception as e:
        plt.close('all')
        raise RuntimeError(f"创建箱线图幻灯片时出错: {e}") from e
