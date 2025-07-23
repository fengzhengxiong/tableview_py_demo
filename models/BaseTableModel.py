#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：BaseTableModel.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:09 
'''

# models/BaseTableModel.py

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

class BaseTableModel(QAbstractTableModel):
    """
    通用的模型基类，封装了数据存储和与视图交互的基础逻辑。
    正确处理begin/end信号，确保视图高效更新。
    """
    def __init__(self, data_list=None, headers=None, parent=None):
        super().__init__(parent)
        self._data = data_list if data_list is not None else []
        self._headers = headers if headers is not None else []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        raise NotImplementedError("Subclasses must implement the data method.")

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    # --- 通用数据操作API ---
    def get_item_by_row(self, row):
        if 0 <= row < self.rowCount():
            return self._data[row]
        return None

    def add_item(self, item_data):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(item_data)
        self.endInsertRows()

    def remove_item_by_row(self, row):
        if 0 <= row < self.rowCount():
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._data[row]
            self.endRemoveRows()
            return True
        return False

    def find_row_by_id(self, item_id):
        for i, item in enumerate(self._data):
            # 确保item有id属性
            if hasattr(item, 'id') and item.id == item_id:
                return i
        return -1

    def clear(self):
        self.beginResetModel()
        self._data = []
        self.endResetModel()