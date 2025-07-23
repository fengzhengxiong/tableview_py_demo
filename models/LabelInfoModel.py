#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：LabelInfoModel.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:10 
'''

# models/LabelInfoModel.py

from PySide6.QtCore import Qt, QModelIndex
from .BaseTableModel import BaseTableModel

COL_LBL_ID, COL_LBL_NAME, COL_LBL_TYPE, COL_LBL_OP = range(4)

class LabelInfoModel(BaseTableModel):
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid(): return None
        row_data = self.get_item_by_row(index.row())
        if not row_data: return None

        column = index.column()
        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if column == COL_LBL_ID: return str(index.row() + 1)
            if column == COL_LBL_NAME: return row_data.label_name
            if column == COL_LBL_TYPE: return row_data.label_type
            return ""
        if role == Qt.ForegroundRole: return row_data.item_color
        if role == Qt.TextAlignmentRole: return Qt.AlignCenter
        if role == Qt.UserRole: return row_data
        if role == Qt.UserRole + 1 and column == COL_LBL_OP:
            return row_data.is_visible
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or role != Qt.EditRole or index.column() != COL_LBL_OP:
            return False

        row_data = self.get_item_by_row(index.row())
        if not row_data: return False

        row_data.is_visible = bool(value)
        self.dataChanged.emit(index, index, [role, Qt.UserRole + 1])
        return True

    def toggle_visibility(self, row: int) -> tuple[bool, bool]:
        if not (0 <= row < self.rowCount()): return False, False

        current_visibility = self.get_item_by_row(row).is_visible
        new_visibility = not current_visibility

        index = self.index(row, COL_LBL_OP)
        success = self.setData(index, new_visibility, Qt.EditRole)
        return success, new_visibility