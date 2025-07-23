#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：CustomDelegate.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:08 
'''

# delegates/CustomDelegate.py

from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import Qt, QRect, QSortFilterProxyModel
from PySide6.QtGui import QIcon, QColor

from models.FileTableModel import COL_OP as FILE_COL_OP
from models.LabelInfoModel import COL_LBL_OP
from models.LabelTypeModel import COL_TYP_COLOR, COL_TYP_OP


class CustomDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icons = {
            "delete": QIcon("icons/delete.png").pixmap(16, 16),
            "view": QIcon("icons/view.png").pixmap(16, 16),
            "unview": QIcon("icons/unview.png").pixmap(16, 16)
        }

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        # model_name = index.model().__class__.__name__
        # --- 关键修正：获取真正的源模型 ---
        model = index.model()
        source_model = None

        if isinstance(model, QSortFilterProxyModel):
            # 如果当前模型是代理模型，则获取其源模型
            source_model = model.sourceModel()
        else:
            # 否则，当前模型就是源模型
            source_model = model

        model_name = source_model.__class__.__name__
        # --- 修正结束 ---

        column = index.column()

        if model_name == "FileTableModel":
            if column == FILE_COL_OP:
                self._draw_icon(painter, option.rect, self.icons["delete"])
            return

        if model_name == "LabelInfoModel":
            if column == COL_LBL_OP:
                is_visible = index.data(Qt.UserRole + 1)
                icon = self.icons["view"] if is_visible else self.icons["unview"]
                self._draw_icon(painter, option.rect, icon)
            return

        if model_name == "LabelTypeModel":
            if column == COL_TYP_COLOR:
                color = index.data(Qt.ForegroundRole)
                if isinstance(color, QColor):
                    color_rect = option.rect.adjusted(5, 5, -5, -5)
                    painter.fillRect(color_rect, color)
            elif column == COL_TYP_OP:
                self._draw_icon(painter, option.rect, self.icons["delete"])
            return

    def _draw_icon(self, painter, cell_rect, icon_pixmap):
        icon_rect = self._get_centered_rect(cell_rect, icon_pixmap.size())
        painter.drawPixmap(icon_rect.topLeft(), icon_pixmap)

    def _get_centered_rect(self, cell_rect: QRect, item_size) -> QRect:
        x = cell_rect.x() + (cell_rect.width() - item_size.width()) / 2
        y = cell_rect.y() + (cell_rect.height() - item_size.height()) / 2
        return QRect(int(x), int(y), item_size.width(), item_size.height())