# 自动生成数据分析报告（PPT格式）

一个使用 Python 自动化生成数据分析报告（PPT 格式）的工具库。

----------

## 目录

- [功能特点](#功能特点)
- [安装依赖](#安装依赖)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [命令行用法](#命令行用法)
- [API 文档](#api-文档)
- [数据格式要求](#数据格式要求)
- [模板说明](#模板说明)
- [运行测试](#运行测试)
- [版本历史](#版本历史)
- [相关文章](#相关文章)

----------

## 功能特点

- ✅ **数据可视化**：支持箱线图、散点图、趋势图等多种图表类型
- ✅ **PPT 自动化**：使用 python-pptx 自动创建和编辑 PPT 幻灯片
- ✅ **命令行工具**：提供简单易用的命令行接口
- ✅ **类型注解**：所有函数都添加了完整的类型注解
- ✅ **异常处理**：完善的错误处理和异常提示
- ✅ **模板支持**：支持自定义 PPT 模板

----------

## 安装依赖

### 方法一：使用 requirements.txt（推荐）

```bash
pip install -r requirements.txt
```

### 方法二：手动安装

```bash
pip install python-pptx pandas openpyxl xlwt matplotlib seaborn
```

### 可选依赖（Selenium 功能）

如果需要使用网页自动化功能：

```bash
pip install selenium webdriver-manager
```

----------

## 快速开始

### 最简单的用法

直接运行 `main.py`，使用默认配置生成报告：

```bash
python main.py
```

### 指定数据文件和输出路径

```bash
python main.py --data resources/data/data0.xlsx --output my_report.pptx
```

### 只生成特定类型的图表

```bash
python main.py --charts summary boxplot lineplot
```

### 查看帮助信息

```bash
python main.py --help
```

----------

## 项目结构

```
py-pptx/
├── auto_report/                 # 核心代码目录
│   ├── __init__.py
│   ├── hello_data.py           # 数据分析和可视化类
│   ├── hello_pptx.py           # PPT 操作模块
│   ├── hello_selenium.py       # 网页自动化模块
│   └── hello_plot_date.py      # 日期序列图绘制模块
│
├── resources/                   # 资源目录
│   ├── data/                   # 数据文件存放目录
│   │   └── data0.xlsx          # 示例数据文件
│   ├── driver/                 # 浏览器驱动位置
│   ├── report/                 # 报告生成位置
│   │   └── .gitignore
│   └── template/               # PPT 报告模板
│       ├── ppt_template0.pptx
│       └── ppt_template1.pptx
│
├── tests/                       # 测试代码目录
│   ├── __init__.py
│   ├── test_hello_data.py      # 测试 hello_data 模块
│   ├── test_hello_pptx.py      # 测试 hello_pptx 模块
│   ├── test_hello_selenium.py  # 测试 hello_selenium 模块
│   └── test_main.py            # 主测试运行器
│
├── main.py                      # 命令行入口文件
├── requirements.txt             # 项目依赖列表
└── README.md                    # 本说明文档
```

----------

## 命令行用法

### 完整参数列表

```bash
python main.py [OPTIONS]
```

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--version` | `-v` | - | 显示版本号 |
| `--data` | `-d` | `resources/data/data0.xlsx` | Excel 数据文件路径 |
| `--template` | `-t` | `resources/template/ppt_template0.pptx` | PPT 模板文件路径 |
| `--output` | `-o` | 自动生成 | 输出 PPT 文件路径 |
| `--charts` | `-c` | 所有图表 | 要生成的图表类型（可多选） |
| `--list-charts` | - | - | 列出可用的图表类型 |
| `--help` | `-h` | - | 显示帮助信息 |

### 可用的图表类型

使用 `--list-charts` 查看所有可用的图表类型：

```bash
python main.py --list-charts
```

输出：
```
可用的图表类型:
  summary   - 数据概览
  boxplot   - 箱线图（垂直）
  boxplot_h - 箱线图（水平）
  stripplot - 散点图
  lineplot  - 趋势图
```

### 使用示例

#### 示例 1：使用默认配置

```bash
python main.py
```

这将：
- 从 `resources/data/data0.xlsx` 加载数据
- 使用 `resources/template/ppt_template0.pptx` 作为模板
- 在 `resources/report/` 目录下生成带时间戳的报告文件
- 包含所有可用的图表类型

#### 示例 2：自定义输出路径

```bash
python main.py --output my_analysis.pptx
```

报告将保存为当前目录下的 `my_analysis.pptx`。

#### 示例 3：使用自定义模板

```bash
python main.py --template resources/template/ppt_template1.pptx
```

#### 示例 4：只生成特定图表

```bash
# 只生成数据概览和箱线图
python main.py --charts summary boxplot

# 生成所有图表类型
python main.py
```

#### 示例 5：完整的自定义配置

```bash
python main.py \
  --data my_data.xlsx \
  --template my_template.pptx \
  --output my_report.pptx \
  --charts summary boxplot lineplot
```

----------

## API 文档

### ReportGenerator 类

`ReportGenerator` 是主要的报告生成类。

```python
from main import ReportGenerator

# 创建报告生成器实例
generator = ReportGenerator(
    data_path='resources/data/data0.xlsx',
    template_path='resources/template/ppt_template0.pptx',
    output_path='my_report.pptx'
)

# 生成完整报告
output_path = generator.generate_report()

# 只生成特定图表
output_path = generator.generate_report(chart_types=['summary', 'boxplot'])
```

#### 主要方法

| 方法 | 说明 |
|------|------|
| `__init__(data_path, template_path, output_path)` | 初始化报告生成器 |
| `generate_report(chart_types)` | 生成完整的 PPT 报告 |

### HelloData 类

`HelloData` 类用于数据分析和可视化。

```python
from auto_report.hello_data import HelloData

# 创建实例
data = HelloData('resources/data/data0.xlsx', 'Sheet1')

# 获取 DataFrame
df = data.dataframe

# 绘制箱线图
fig = data.seaborn_boxplot1()

# 绘制散点图
fig = data.seaborn_stripplot()

# 绘制趋势图
fig = data.df_pivot_table()
```

#### 主要方法

| 方法 | 说明 |
|------|------|
| `__init__(wbk, sheet)` | 从 Excel 文件加载数据 |
| `dataframe` | 获取加载的数据 DataFrame |
| `seaborn_boxplot1()` | 绘制垂直箱线图（方法1） |
| `seaborn_boxplot2()` | 绘制垂直箱线图（方法2） |
| `seaborn_boxplot3()` | 绘制水平箱线图 |
| `seaborn_pointplot()` | 绘制点图 |
| `seaborn_stripplot()` | 绘制散点图 |
| `df_pivot_table()` | 绘制分组折线图（趋势图） |

### hello_pptx 模块

`hello_pptx` 模块提供 PPT 操作功能。

```python
from auto_report.hello_pptx import (
    ensure_report_dir,
    add_all_slide_layout,
    page1_boxplot,
    SLIDE_LAYOUT_NAMES
)
from pptx import Presentation

# 创建演示文稿
prs = Presentation()

# 添加所有幻灯片布局
slides = add_all_slide_layout(prs)

# 添加箱线图幻灯片
slide = page1_boxplot(prs)

# 保存
prs.save('output.pptx')
```

#### 主要函数

| 函数 | 说明 |
|------|------|
| `ensure_report_dir()` | 确保报告目录存在 |
| `add_all_slide_layout(prs)` | 为演示文稿添加所有类型的幻灯片布局 |
| `add_text_by_shape(slide)` | 通过遍历形状添加文本 |
| `add_text_by_palceholder(slide)` | 通过遍历占位符添加文本 |
| `page1_boxplot(prs, data_path)` | 添加包含箱线图的幻灯片 |

#### 幻灯片布局常量

```python
SLIDE_LAYOUT_NAMES = {
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
```

----------

## 数据格式要求

### Excel 文件结构

项目默认使用 `resources/data/data0.xlsx` 文件，数据应位于名为 `Sheet1` 的工作表中。

### 必需的列

数据文件应包含以下列（可根据实际情况调整）：

| 列名 | 类型 | 说明 |
|------|------|------|
| `Project` | 字符串 | 项目名称（用于分组） |
| `Lead Time` | 数值 | 交付周期（Y 轴数据） |
| `Story完成时间` | 日期/时间 | 时间（X 轴数据） |

### 示例数据

| Project | Story完成时间 | Lead Time |
|---------|---------------|-----------|
| 项目A | 2018-01-01 | 5 |
| 项目A | 2018-01-02 | 7 |
| 项目B | 2018-01-01 | 3 |
| 项目B | 2018-01-02 | 6 |
| ... | ... | ... |

### 自定义数据

如果你有不同格式的数据，可以：

1. 修改 `main.py` 中的 `ReportGenerator` 类，调整列名
2. 直接使用 `HelloData` 类，自行处理数据和绘图

----------

## 模板说明

项目提供了两个 PPT 模板：

- `ppt_template0.pptx` - 默认模板
- `ppt_template1.pptx` - 备用模板

### 模板要求

模板应包含以下幻灯片布局（至少需要前 6 个布局）：

| 布局索引 | 用途 |
|----------|------|
| 0 | 标题幻灯片 |
| 1 | 标题和内容 |
| 5 | 仅标题（用于图片幻灯片） |
| 6 | 空白 |

### 创建自定义模板

1. 打开 PowerPoint
2. 视图 → 幻灯片母版
3. 设计你的模板样式
4. 确保包含所需的布局
5. 保存为 `.pptx` 文件
6. 使用 `--template` 参数指定

----------

## 运行测试

### 运行所有测试

```bash
cd tests
python test_main.py
```

或

```bash
python -m pytest tests/ -v
```

### 运行特定测试文件

```bash
python -m pytest tests/test_hello_data.py -v
python -m pytest tests/test_hello_pptx.py -v
```

### 测试说明

- `test_hello_data.py` - 测试数据加载和绘图功能
- `test_hello_pptx.py` - 测试 PPT 操作功能
- `test_hello_selenium.py` - 测试 Selenium 相关功能（需要浏览器）

**注意**：Selenium 测试需要 Chrome 浏览器，并且可能需要网络连接。

----------

## 版本历史

### v1.0.0 (2026-04-22)

- ✨ 新增 `main.py` 命令行入口文件
- ✨ 新增 `ReportGenerator` 类，支持完整的报告生成流程
- ✨ 支持命令行参数解析（argparse）
- ✨ 支持多种图表类型：summary、boxplot、boxplot_h、stripplot、lineplot
- ✨ 支持自定义数据文件、模板文件、输出路径
- 🔧 所有模块添加了完整的类型注解
- 🔧 所有模块添加了详细的文档字符串
- 🔧 所有模块添加了全面的异常处理
- 🔧 测试用例优化（使用 unittest 标准生命周期方法）
- 🔧 修复了 Selenium 4.x API 兼容性问题
- 🔧 修复了相对路径问题
- 🔧 修复了 matplotlib 状态污染问题
- 📝 更新了 `README.md`，添加完整的中文使用说明
- 📝 创建了 `requirements.txt`，记录所有依赖

----------

## 相关文章

本项目是系列文章的配套代码：

1. **[自动生成数据分析报告（1）：Hello python-pptx](https://mp.weixin.qq.com/s/GOnRpruOCgIpshyxtFQV1g)**
   - 介绍 python-pptx 基础用法

2. **[自动生成数据分析报告（2）：Hello 箱线图）：Hello python-pptx](https://mp.weixin.qq.com/s/JExi5eSW4fZo2V_Sw7IbiA)**
   - 数据可视化与箱线图

3. **[自动生成数据分析报告（3）：Hello PPT 模板）：Hello python-pptx](https://mp.weixin.qq.com/s/U5l-POtdunHQ0zqpcFZBGg)**
   - 使用 PPT 模板

4. **[自动生成数据分析报告（4）：Hello 分组箱线图）：Hello python-pptx](https://mp.weixin.qq.com/s/4LdxPj4PJqRaNTK0Esv33Q)**
   - 分组箱线图

5. **[自动生成数据分析报告（5）：Hello selenium）：Hello python-pptx](https://mp.weixin.qq.com/s/0X0J_A106v79LAUfgTka9g)**
   - 网页数据抓取

----------

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

----------

**注意**：`hello_selenium.py` 中的 `get_house365_today_info()` 函数已标记为废弃，因为目标网站结构可能已经变化。如需使用 Selenium 功能，请参考 `create_chrome_driver()` 函数自行实现。
