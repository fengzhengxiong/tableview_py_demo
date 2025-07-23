#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：ImageInfoModel.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:10 
'''

# models/ImageInfoModel.py

from PySide6.QtCore import Qt, QModelIndex
from .BaseTableModel import BaseTableModel

COL_NAME, COL_CATEGORY, COL_RESOLUTION = range(3)

class ImageInfoModel(BaseTableModel):
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid(): return None
        row_data = self.get_item_by_row(index.row())
        if not row_data: return None

        column = index.column()

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if column == COL_NAME: return row_data.file_image_name
            if column == COL_CATEGORY: return row_data.project_category
            if column == COL_RESOLUTION: return row_data.file_image_resolution
        if role == Qt.ForegroundRole: return row_data.item_color
        if role == Qt.TextAlignmentRole: return Qt.AlignCenter
        return None