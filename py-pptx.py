# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 12:12:34 2018

@author: Administrator
"""

from pptx import Presentation

# 使用自定义模板
prs = Presentation('./template/ppt_template0.pptx')

# slide_layouts[1]为带标题和正文框的ppt
title_slide_layout = prs.slide_layouts[1]

# 新增ppt（当前仅支持新增操作）
slide = prs.slides.add_slide(title_slide_layout)

# 取本页ppt的title，向title文本框写如文字 
title = slide.shapes.title
title.text = 'this is a title' 

# 取出本页第二个文本框，在第二个文本框中写入文字
subtitle = slide.shapes.placeholders[1]   
subtitle.text = 'this is a subtitle'   

# 保存ppt
prs.save('数据分析报告.pptx')