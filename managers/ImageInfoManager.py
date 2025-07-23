#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：ImageInfoManager.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:08 
'''

# managers/ImageInfoManager.py

from PySide6.QtWidgets import QWidget, QVBoxLayout

from models.ImageInfoModel import ImageInfoModel
from views.BaseTableView import BaseTableView
from data.TableDataStruct import ImageInfoDataStruct

class ImageInfoManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_model_view()
        self._init_ui()

    def _init_model_view(self):
        headers = ["图片名称", "项目类别", "图片分辨率"]
        self.model = ImageInfoModel(headers=headers)
        self.view = BaseTableView(column_width_ratios=[1, 1, 1])
        self.view.setModel(self.model)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        layout.addWidget(self.view)

    def display_info(self, info: ImageInfoDataStruct):
        self.model.clear()

        if info:
            self.model.add_item(
                ImageInfoDataStruct(
                    file_image_name = info.file_image_name,
                    project_category = "实例分割",
                    file_image_resolution = "1920x1080"
                )
            )

    def clear_info(self):
        self.model.clear()