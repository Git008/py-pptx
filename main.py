# -*- coding: utf-8 -*-
"""
自动生成数据分析报告（PPT格式）- 主入口文件

提供命令行接口，支持从 Excel 数据生成包含各种图表的 PPT 报告。

用法示例:
    python main.py --data resources/data/data0.xlsx --output report.pptx
    python main.py --help
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from typing import Optional, List, Dict, Any, TYPE_CHECKING

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

if TYPE_CHECKING:
    from matplotlib.figure import Figure
    from pptx.presentation import Presentation as PresentationType
    from pptx.slide import Slide

__version__ = '1.0.0'
__author__ = 'py-pptx Team'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(PROJECT_ROOT, 'resources')
DATA_DIR = os.path.join(RESOURCES_DIR, 'data')
REPORT_DIR = os.path.join(RESOURCES_DIR, 'report')
TEMPLATE_DIR = os.path.join(RESOURCES_DIR, 'template')

DEFAULT_TEMPLATE = os.path.join(TEMPLATE_DIR, 'ppt_template0.pptx')
DEFAULT_DATA = os.path.join(DATA_DIR, 'data0.xlsx')
DEFAULT_OUTPUT = os.path.join(REPORT_DIR, f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pptx')


class ReportGenerator:
    """
    PPT 报告生成器类。
    
    负责从数据生成图表并创建 PPT 报告。
    
    Attributes:
        data_path: 数据文件路径
        template_path: PPT 模板路径
        output_path: 输出文件路径
        df: 加载的数据 DataFrame
        prs: PPT 演示文稿对象
    """
    
    def __init__(
        self,
        data_path: str,
        template_path: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> None:
        """
        初始化报告生成器。
        
        Args:
            data_path: Excel 数据文件路径
            template_path: PPT 模板文件路径（可选）
            output_path: 输出文件路径（可选）
        
        Raises:
            FileNotFoundError: 如果数据文件或模板文件不存在
        """
        self.data_path = data_path
        self.template_path = template_path or DEFAULT_TEMPLATE
        self.output_path = output_path or DEFAULT_OUTPUT
        
        self.df: Optional[pd.DataFrame] = None
        self.prs: Optional[PresentationType] = None
        self._temp_images: List[str] = []
        
        self._validate_paths()
        self._load_data()
        self._load_template()
    
    def _validate_paths(self) -> None:
        """
        验证文件路径是否存在。
        
        Raises:
            FileNotFoundError: 如果数据文件或模板文件不存在
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"数据文件不存在: {self.data_path}")
        
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"模板文件不存在: {self.template_path}")
        
        output_dir = os.path.dirname(self.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
    
    def _load_data(self) -> None:
        """
        加载 Excel 数据文件。
        
        Raises:
            ValueError: 如果数据文件为空或格式错误
            ImportError: 如果缺少依赖
        """
        try:
            self.df = pd.read_excel(self.data_path, sheet_name='Sheet1')
            
            if self.df.empty:
                raise ValueError("数据文件为空")
                
        except FileNotFoundError:
            raise
        except ValueError as ve:
            if "Worksheet named" in str(ve) and "not found" in str(ve):
                raise ValueError("工作表 'Sheet1' 不存在于文件中") from ve
            raise
        except ImportError as ie:
            if "openpyxl" in str(ie):
                raise ImportError(
                    "缺少 openpyxl 依赖，请运行: pip install openpyxl>=3.1.5"
                ) from ie
            raise
        except Exception as e:
            raise RuntimeError(f"加载数据文件时出错: {e}") from e
    
    def _load_template(self) -> None:
        """
        加载 PPT 模板文件。
        
        Raises:
            RuntimeError: 如果加载模板失败
        """
        try:
            self.prs = Presentation(self.template_path)
        except Exception as e:
            raise RuntimeError(f"加载 PPT 模板时出错: {e}") from e
    
    def _add_title_slide(self, title: str, subtitle: Optional[str] = None) -> Slide:
        """
        添加标题幻灯片。
        
        Args:
            title: 主标题
            subtitle: 副标题（可选）
        
        Returns:
            Slide: 新创建的幻灯片
        """
        if len(self.prs.slide_layouts) < 1:
            raise ValueError("模板缺少标题幻灯片布局")
        
        slide_layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(slide_layout)
        
        title_shape = slide.shapes.title
        if title_shape is not None:
            title_shape.text = title
        
        if subtitle and len(slide.placeholders) > 1:
            subtitle_shape = slide.placeholders[1]
            if subtitle_shape.has_text_frame:
                subtitle_shape.text = subtitle
        
        return slide
    
    def _add_content_slide(self, title: str, content: Optional[str] = None) -> Slide:
        """
        添加内容幻灯片。
        
        Args:
            title: 幻灯片标题
            content: 内容文本（可选）
        
        Returns:
            Slide: 新创建的幻灯片
        """
        if len(self.prs.slide_layouts) < 2:
            raise ValueError("模板缺少内容幻灯片布局")
        
        slide_layout = self.prs.slide_layouts[1]
        slide = self.prs.slides.add_slide(slide_layout)
        
        title_shape = slide.shapes.title
        if title_shape is not None:
            title_shape.text = title
        
        if content and len(slide.placeholders) > 1:
            content_shape = slide.placeholders[1]
            if content_shape.has_text_frame:
                content_shape.text = content
        
        return slide
    
    def _add_picture_slide(
        self,
        title: str,
        image_path: str,
        left: float = 1.0,
        top: float = 1.5,
        width: float = 8.0,
        height: float = 4.5
    ) -> Slide:
        """
        添加包含图片的幻灯片。
        
        Args:
            title: 幻灯片标题
            image_path: 图片文件路径
            left: 左边距（英寸）
            top: 上边距（英寸）
            width: 图片宽度（英寸）
            height: 图片高度（英寸）
        
        Returns:
            Slide: 新创建的幻灯片
        """
        if len(self.prs.slide_layouts) < 6:
            raise ValueError("模板缺少空白幻灯片布局")
        
        slide_layout = self.prs.slide_layouts[5]
        slide = self.prs.slides.add_slide(slide_layout)
        
        title_shape = slide.shapes.title
        if title_shape is not None:
            title_shape.text = title
        
        slide.shapes.add_picture(
            image_path,
            Inches(left),
            Inches(top),
            Inches(width),
            Inches(height)
        )
        
        return slide
    
    def _generate_boxplot(
        self,
        x_col: str,
        y_col: str,
        title: str,
        output_path: str,
        horizontal: bool = False
    ) -> str:
        """
        生成箱线图。
        
        Args:
            x_col: X 轴列名
            y_col: Y 轴列名
            title: 图表标题
            output_path: 输出图片路径
            horizontal: 是否水平显示
        
        Returns:
            str: 生成的图片路径
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if horizontal:
            sns.boxplot(x=self.df[y_col], y=self.df[x_col], orient='h', ax=ax)
        else:
            sns.boxplot(x=self.df[x_col], y=self.df[y_col], ax=ax)
        
        ax.set_title(title)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        plt.tight_layout()
        
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close('all')
        
        return output_path
    
    def _generate_stripplot(
        self,
        x_col: str,
        y_col: str,
        hue_col: str,
        title: str,
        output_path: str
    ) -> str:
        """
        生成散点图。
        
        Args:
            x_col: X 轴列名
            y_col: Y 轴列名
            hue_col: 颜色分组列名
            title: 图表标题
            output_path: 输出图片路径
        
        Returns:
            str: 生成的图片路径
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        sns.stripplot(x=x_col, y=y_col, hue=hue_col, data=self.df, ax=ax)
        
        ax.set_title(title)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        
        plt.gcf().autofmt_xdate()
        plt.legend(bbox_to_anchor=(1.02, 1.0), borderaxespad=0, loc='upper left')
        plt.tight_layout()
        plt.subplots_adjust(right=0.8)
        
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close('all')
        
        return output_path
    
    def _generate_lineplot(
        self,
        index_col: str,
        value_col: str,
        group_col: str,
        title: str,
        output_path: str
    ) -> str:
        """
        生成分组折线图。
        
        Args:
            index_col: 索引列名
            value_col: 值列名
            group_col: 分组列名
            title: 图表标题
            output_path: 输出图片路径
        
        Returns:
            str: 生成的图片路径
        """
        pivot = self.df.pivot_table(
            index=[index_col],
            columns=group_col,
            values=value_col
        )
        
        ax = pivot.plot(title=title, style='-o', figsize=(12, 6))
        ax.set_xlabel(index_col)
        ax.set_ylabel(value_col)
        
        plt.legend(bbox_to_anchor=(1.02, 1.0), borderaxespad=0, loc='upper left')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.subplots_adjust(right=0.8)
        
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close('all')
        
        return output_path
    
    def _generate_summary_slide(self) -> Slide:
        """
        生成数据汇总幻灯片。
        
        Returns:
            Slide: 新创建的幻灯片
        """
        if self.df is None:
            raise ValueError("数据未加载")
        
        summary_lines = [
            f"数据总行数: {len(self.df)}",
            f"数据列数: {len(self.df.columns)}",
            f"列名: {', '.join(self.df.columns)}",
        ]
        
        if 'Project' in self.df.columns:
            project_counts = self.df['Project'].value_counts()
            summary_lines.append(f"\n项目分布:")
            for proj, count in project_counts.items():
                summary_lines.append(f"  - {proj}: {count} 条")
        
        if 'Lead Time' in self.df.columns:
            summary_lines.append(f"\nLead Time 统计:")
            summary_lines.append(f"  - 平均值: {self.df['Lead Time'].mean():.2f}")
            summary_lines.append(f"  - 中位数: {self.df['Lead Time'].median():.2f}")
            summary_lines.append(f"  - 最小值: {self.df['Lead Time'].min()}")
            summary_lines.append(f"  - 最大值: {self.df['Lead Time'].max()}")
        
        content = "\n".join(summary_lines)
        return self._add_content_slide("数据概览", content)
    
    def generate_report(self, chart_types: Optional[List[str]] = None) -> str:
        """
        生成完整的 PPT 报告。
        
        Args:
            chart_types: 要生成的图表类型列表。可选值:
                'boxplot', 'boxplot_h', 'stripplot', 'lineplot', 'summary'
                如果为 None，则生成所有可用图表。
        
        Returns:
            str: 生成的 PPT 文件路径
        
        Raises:
            ValueError: 如果数据未加载
            RuntimeError: 如果生成报告过程中出错
        """
        if self.df is None or self.prs is None:
            raise ValueError("数据或模板未加载")
        
        if chart_types is None:
            chart_types = ['summary', 'boxplot', 'boxplot_h', 'stripplot', 'lineplot']
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            self._add_title_slide(
                "数据分析报告",
                f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            for chart_type in chart_types:
                if chart_type == 'summary':
                    self._generate_summary_slide()
                    
                elif chart_type == 'boxplot':
                    if 'Project' in self.df.columns and 'Lead Time' in self.df.columns:
                        img_path = os.path.join(REPORT_DIR, f'boxplot_{timestamp}.png')
                        self._temp_images.append(img_path)
                        self._generate_boxplot(
                            'Project', 'Lead Time',
                            'Lead Time 箱线图（按 Project 分组）',
                            img_path
                        )
                        self._add_picture_slide('箱线图分析', img_path)
                        
                elif chart_type == 'boxplot_h':
                    if 'Project' in self.df.columns and 'Lead Time' in self.df.columns:
                        img_path = os.path.join(REPORT_DIR, f'boxplot_h_{timestamp}.png')
                        self._temp_images.append(img_path)
                        self._generate_boxplot(
                            'Project', 'Lead Time',
                            'Lead Time 水平箱线图',
                            img_path,
                            horizontal=True
                        )
                        self._add_picture_slide('水平箱线图分析', img_path)
                        
                elif chart_type == 'stripplot':
                    if all(col in self.df.columns for col in ['Story完成时间', 'Lead Time', 'Project']):
                        img_path = os.path.join(REPORT_DIR, f'stripplot_{timestamp}.png')
                        self._temp_images.append(img_path)
                        self._generate_stripplot(
                            'Story完成时间', 'Lead Time', 'Project',
                            'Lead Time 散点图（按 Project 着色）',
                            img_path
                        )
                        self._add_picture_slide('散点图分析', img_path)
                        
                elif chart_type == 'lineplot':
                    if all(col in self.df.columns for col in ['Story完成时间', 'Lead Time', 'Project']):
                        img_path = os.path.join(REPORT_DIR, f'lineplot_{timestamp}.png')
                        self._temp_images.append(img_path)
                        self._generate_lineplot(
                            'Story完成时间', 'Lead Time', 'Project',
                            'Lead Time 趋势图',
                            img_path
                        )
                        self._add_picture_slide('趋势图分析', img_path)
            
            self.prs.save(self.output_path)
            
            self._cleanup_temp_images()
            
            return self.output_path
            
        except Exception as e:
            self._cleanup_temp_images()
            raise RuntimeError(f"生成报告时出错: {e}") from e
    
    def _cleanup_temp_images(self) -> None:
        """
        清理临时生成的图片文件。
        """
        for img_path in self._temp_images:
            try:
                if os.path.exists(img_path):
                    os.remove(img_path)
            except Exception:
                pass
        self._temp_images = []


def create_parser() -> argparse.ArgumentParser:
    """
    创建命令行参数解析器。
    
    Returns:
        argparse.ArgumentParser: 参数解析器
    """
    parser = argparse.ArgumentParser(
        prog='py-pptx',
        description='自动生成数据分析报告（PPT格式）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  # 使用默认配置生成报告
  python main.py
  
  # 指定数据文件和输出路径
  python main.py --data resources/data/data0.xlsx --output my_report.pptx
  
  # 指定模板文件
  python main.py --template resources/template/ppt_template1.pptx
  
  # 只生成特定类型的图表
  python main.py --charts summary boxplot lineplot
        '''
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '-d', '--data',
        type=str,
        default=DEFAULT_DATA,
        help=f'Excel 数据文件路径（默认: {DEFAULT_DATA}）'
    )
    
    parser.add_argument(
        '-t', '--template',
        type=str,
        default=DEFAULT_TEMPLATE,
        help=f'PPT 模板文件路径（默认: {DEFAULT_TEMPLATE}）'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='输出 PPT 文件路径（默认: 自动生成带时间戳的文件名）'
    )
    
    parser.add_argument(
        '-c', '--charts',
        type=str,
        nargs='+',
        choices=['summary', 'boxplot', 'boxplot_h', 'stripplot', 'lineplot'],
        default=None,
        help='要生成的图表类型（默认: 生成所有可用图表）'
    )
    
    parser.add_argument(
        '--list-charts',
        action='store_true',
        help='列出可用的图表类型'
    )
    
    return parser


def list_available_charts() -> None:
    """
    列出可用的图表类型。
    """
    print("可用的图表类型:")
    print("  summary   - 数据概览")
    print("  boxplot   - 箱线图（垂直）")
    print("  boxplot_h - 箱线图（水平）")
    print("  stripplot - 散点图")
    print("  lineplot  - 趋势图")


def main() -> int:
    """
    主函数。
    
    Returns:
        int: 退出码（0 表示成功，非 0 表示失败）
    """
    parser = create_parser()
    args = parser.parse_args()
    
    if args.list_charts:
        list_available_charts()
        return 0
    
    try:
        print(f"数据文件: {args.data}")
        print(f"模板文件: {args.template}")
        if args.output:
            print(f"输出文件: {args.output}")
        if args.charts:
            print(f"图表类型: {', '.join(args.charts)}")
        print()
        
        generator = ReportGenerator(
            data_path=args.data,
            template_path=args.template,
            output_path=args.output
        )
        
        print("正在生成报告...")
        output_path = generator.generate_report(chart_types=args.charts)
        
        print(f"\n报告已成功生成: {output_path}")
        return 0
        
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"数据错误: {e}", file=sys.stderr)
        return 1
    except ImportError as e:
        print(f"依赖错误: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"运行时错误: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
