#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：TableDataStruct.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:07 
'''

# data/TableDataStruct.py

import uuid
from PySide6.QtGui import QColor

# --- 通用颜色定义 ---
default_color = QColor("black")
train_color = QColor("#3498db")  # 蓝色
val_color = QColor("#2ecc71")    # 绿色
saved_color = QColor("#9b59b6")  # 紫色

# --- 数据结构定义 ---

class FileDataStruct:
    """文件信息的数据结构。这是一个纯粹的数据容器。"""
    def __init__(self, file_image_name: str, file_image_state: str, color: QColor = default_color, file_id: str = None):
        self.id = file_id if file_id is not None else str(uuid.uuid4())
        self.file_image_name = file_image_name
        self.file_image_state = file_image_state
        self.item_color = color

class ImageInfoDataStruct:
    """图片详细信息的数据结构。"""
    def __init__(self, file_image_name: str, project_category: str, file_image_resolution: str, color: QColor = default_color):
        self.file_image_name = file_image_name
        self.project_category = project_category
        self.file_image_resolution = file_image_resolution
        self.item_color = color

class LabelInfoDataStruct:
    """单个标签信息的数据结构。"""
    def __init__(self, label_name: str, label_type: str, color: QColor = default_color, label_id: str = None):
        self.id = label_id if label_id is not None else str(uuid.uuid4())
        self.label_name = label_name
        self.label_type = label_type
        self.item_color = color
        self.is_visible = True

class LabelTypeDataStruct:
    """标签类别信息的数据结构。"""
    def __init__(self, label_type_name: str, color: QColor, type_id: str = None):
        self.id = type_id if type_id is not None else str(uuid.uuid4())
        self.label_type_name = label_type_name
        self.color = color