#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：LabelInfoManager.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:08 
'''

# managers/LabelInfoManager.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal, QModelIndex, Qt
from models.LabelInfoModel import LabelInfoModel, COL_LBL_OP
from views.BaseTableView import BaseTableView
from delegates.CustomDelegate import CustomDelegate
from data.TableDataStruct import LabelInfoDataStruct


class LabelInfoManager(QWidget):
    visibilityChanged = Signal(str, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_model_view()
        self._init_ui()
        self._connect_signals()

    def _init_model_view(self):
        headers = ["序号", "标签名称", "标签类别", "操作"]
        self.model = LabelInfoModel(headers=headers)
        self.view = BaseTableView(column_width_ratios=[1, 4, 4, 1])
        self.delegate = CustomDelegate(self)
        self.view.setModel(self.model)
        self.view.setItemDelegateForColumn(COL_LBL_OP, self.delegate)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        layout.addWidget(self.view)

    def _connect_signals(self):
        self.view.clicked.connect(self.on_view_clicked)

    def on_view_clicked(self, index: QModelIndex):
        if index.isValid() and index.column() == COL_LBL_OP:
            success, new_visibility = self.model.toggle_visibility(index.row())
            if success:
                label_data = self.model.data(index, Qt.UserRole)
                if label_data:
                    self.visibilityChanged.emit(label_data.id, new_visibility)

    def set_labels(self, labels: list[LabelInfoDataStruct]):
        self.model.clear()
        for label in labels:
            self.model.add_item(label)

    def clear_labels(self):
        self.model.clear()


