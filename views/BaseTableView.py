#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：BaseTableView.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:10 
'''

# views/BaseTableView.py (修正后)

from PySide6.QtWidgets import QTableView, QHeaderView

class BaseTableView(QTableView):
    """
    表格视图的通用基类。
    - 修正了基于比例设置列宽的逻辑。
    """

    def __init__(self, column_width_ratios=None, parent=None):
        super().__init__(parent)
        self.column_width_ratios = column_width_ratios
        self._init_ui()

    def _init_ui(self):
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setEditTriggers(QTableView.NoEditTriggers)
        self.horizontalHeader().setSectionsMovable(False)

        # 不要在这里设置拉伸，因为 setModel 中会处理
        # 默认情况下，如果无比例，则应该拉伸最后一个 section
        self.horizontalHeader().setStretchLastSection(True)

    def setModel(self, model):
        """
        在设置模型后，应用列宽策略。
        """
        super().setModel(model)
        if self.column_width_ratios and self.column_width_ratios and model.columnCount() == len(
                self.column_width_ratios):
            # 关键修正：使用 Interactive 模式，允许我们用代码设置宽度
            self.horizontalHeader().setStretchLastSection(False)  # 当按比例时，禁用最后一行拉伸
            for i in range(model.columnCount()):
                self.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)
            # 立即更新一次列宽
            self._update_column_widths()
        else:
            # 如果没有比例，恢复默认行为
            self.horizontalHeader().setStretchLastSection(True)
            for i in range(model.columnCount()):
                self.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)
                self.horizontalHeader().setSectionResizeMode(model.columnCount() - 1, QHeaderView.Stretch)

    def resizeEvent(self, event):
        """
        窗口大小改变时，重新计算并应用列宽比例。
        """
        super().resizeEvent(event)
        # 只有在设置了比例时才执行
        if self.column_width_ratios:
            self._update_column_widths()

    def _update_column_widths(self):
        """
        辅助函数，用于根据比例计算并设置列宽。
        """
        if not self.model() or not self.column_width_ratios:
            return

        total_ratio = sum(self.column_width_ratios)
        if total_ratio == 0:
            return

        # 使用 viewport 的宽度，这是可用于显示内容的区域
        available_width = self.viewport().width()

        for i, ratio in enumerate(self.column_width_ratios):
            width = int(available_width * ratio / total_ratio)
            self.setColumnWidth(i, width)