#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：FileTableModel.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:10 
'''

# models/FileTableModel.py

from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QColor
from .BaseTableModel import BaseTableModel

COL_ID, COL_NAME, COL_STATE, COL_OP = range(4)

class FileTableModel(BaseTableModel):
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid(): return None
        row_data = self.get_item_by_row(index.row())
        if not row_data: return None

        column = index.column()

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if column == COL_ID: return str(index.row() + 1)
            if column == COL_NAME: return row_data.file_image_name
            if column == COL_STATE: return row_data.file_image_state
            return ""
        if role == Qt.ForegroundRole: return row_data.item_color
        if role == Qt.TextAlignmentRole: return Qt.AlignCenter
        if role == Qt.UserRole: return row_data
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or role != Qt.EditRole: return False
        row_data = self.get_item_by_row(index.row())
        if not row_data: return False

        new_state, new_color = value
        changed = False
        if row_data.file_image_state != new_state:
            row_data.file_image_state = new_state
            changed = True
        if row_data.item_color != new_color:
            row_data.item_color = new_color
            changed = True

        if changed:
            start_index = self.index(index.row(), 0)
            end_index = self.index(index.row(), self.columnCount() - 1)
            self.dataChanged.emit(start_index, end_index, [Qt.DisplayRole, Qt.ForegroundRole])
        return changed

    def update_item_state(self, row: int, new_state: str, new_color: QColor) -> bool:
        if not (0 <= row < self.rowCount()): return False
        index = self.index(row, COL_STATE)
        return self.setData(index, (new_state, new_color), Qt.EditRole)