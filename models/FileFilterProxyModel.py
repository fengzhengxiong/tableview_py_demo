#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：FileFilterProxyModel.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:09 
'''

# models/FileFilterProxyModel.py (重构后)

from PySide6.QtCore import QSortFilterProxyModel, QModelIndex

class FileFilterProxyModel(QSortFilterProxyModel):
    """
    一个被动接收过滤结果的代理模型。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始状态下，不过滤任何东西
        self.accepted_rows = None

    def set_accepted_rows(self, accepted_rows: set):
        """
        从外部设置可接受的行号集合。
        """
        self.accepted_rows = accepted_rows
        # 关键：通知视图过滤器已改变，需要刷新
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        核心过滤逻辑变得极其高效。
        """
        # 如果没有设置过滤集合（例如，搜索框为空），则显示所有行
        if self.accepted_rows is None:
            return True

        # 否则，只检查源行号是否在可接受的集合中
        return source_row in self.accepted_rows