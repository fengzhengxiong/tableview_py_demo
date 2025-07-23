#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：LabelTypeModel.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:10 
'''

# models/LabelTypeModel.py

from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QColor
from .BaseTableModel import BaseTableModel

# 列常量
COL_TYP_NAME, COL_TYP_COLOR, COL_TYP_OP = range(3)

class LabelTypeModel(BaseTableModel):
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid(): return None
        row_data = self.get_item_by_row(index.row())
        if not row_data: return None

        column = index.column()

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if column == COL_TYP_NAME:
                return row_data.label_type_name
            return ""  # 颜色和操作列不显示文本

        # Delegate会使用此颜色来绘制色块
        if role == Qt.ForegroundRole and column == COL_TYP_COLOR:
            return row_data.color

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        if role == Qt.UserRole:
            return row_data

        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        """重写setData以支持通过字典更新数据项"""
        if not index.isValid() or role != Qt.EditRole:
            return False

        row_data = self.get_item_by_row(index.row())
        if not row_data or not isinstance(value, dict):
            return False

        # 从字典中获取新值
        new_name = value.get("name", row_data.label_type_name)
        new_color = value.get("color", row_data.color)

        # 更新数据
        row_data.label_type_name = new_name
        row_data.color = new_color

        # 通知视图整行数据都需要重绘
        start_index = self.index(index.row(), 0)
        end_index = self.index(index.row(), self.columnCount() - 1)
        self.dataChanged.emit(start_index, end_index)
        return True

    # --- 业务逻辑：验证规则 ---
    # 这些方法让模型成为数据完整性的守护者

    def is_name_duplicate(self, name: str, exclude_id: str = None) -> bool:
        """
        检查名称是否重复。
        - name: 要检查的名称。
        - exclude_id: 检查时要排除的项的ID（用于编辑时避免与自身比较）。
        """
        for item in self._data:
            if item.id != exclude_id and item.label_type_name.lower() == name.lower():
                return True
        return False

    def is_color_duplicate(self, color: QColor, exclude_id: str = None) -> bool:
        """
        检查颜色是否重复。
        - color: 要检查的颜色。
        - exclude_id: 检查时要排除的项的ID。
        """
        for item in self._data:
            if item.id != exclude_id and item.color.rgba() == color.rgba():
                return True
        return False