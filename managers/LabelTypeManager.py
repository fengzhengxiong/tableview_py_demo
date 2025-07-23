#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：LabelTypeManager.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:09 
'''

# managers/LabelTypeManager.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                               QInputDialog, QColorDialog, QMessageBox, QMenu)
from PySide6.QtCore import Signal, QModelIndex, Qt, QPoint
from PySide6.QtGui import QColor, QCursor

from models.LabelTypeModel import LabelTypeModel, COL_TYP_OP, COL_TYP_COLOR
from views.BaseTableView import BaseTableView
from delegates.CustomDelegate import CustomDelegate
from data.TableDataStruct import LabelTypeDataStruct


class LabelTypeManager(QWidget):
    # 信号现在更具体，意图更清晰
    labelTypeDeleted = Signal(str)
    labelTypeAdded = Signal(str)
    labelTypeUpdated = Signal(str)
    labelTypeSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_model_view()
        self._init_ui()
        self._connect_signals()
        self._add_initial_types()

    def _init_model_view(self):
        headers = ["标签名称", "标签颜色", "操作"]
        self.model = LabelTypeModel(headers=headers)
        self.view = BaseTableView(column_width_ratios=[2, 1, 1])
        self.delegate = CustomDelegate(self)
        self.view.setModel(self.model)
        self.view.setItemDelegateForColumn(COL_TYP_OP, self.delegate)
        self.view.setItemDelegateForColumn(COL_TYP_COLOR, self.delegate)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        layout.addWidget(self.view)

        self.add_button = QPushButton("添加新类别...")
        layout.addWidget(self.add_button)

        # 启用右键菜单
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)

    def _connect_signals(self):
        self.view.clicked.connect(self.on_view_clicked)
        self.view.customContextMenuRequested.connect(self.show_context_menu)
        self.add_button.clicked.connect(self.add_new_type)

    def _add_initial_types(self):
        initial = [("person", "#e74c3c"), ("car", "#3498db"), ("tree", "#2ecc71")]
        for name, color_hex in initial:
            self.model.add_item(LabelTypeDataStruct(name, QColor(color_hex)))

    # --- 槽函数和交互逻辑 ---

    def on_view_clicked(self, index: QModelIndex):
        """处理单击事件，仅用于发射选中信号。"""
        if not index.isValid():
            return

        type_data = self.model.data(index, Qt.UserRole)
        if type_data:
            # 发射选中信号
            self.labelTypeSelected.emit(type_data.id)

            if index.column() == COL_TYP_OP:
                self.delete_type(index)


    def show_context_menu(self, position: QPoint):
        """显示右键菜单，提供编辑和删除功能。"""
        index = self.view.indexAt(position)
        if not index.isValid():
            return

        menu = QMenu(self.view)
        edit_action = menu.addAction("编辑...")
        delete_action = menu.addAction("删除")

        # 将操作连接到对应的处理函数
        edit_action.triggered.connect(lambda: self.edit_type(index))
        delete_action.triggered.connect(lambda: self.delete_type(index))

        menu.exec(QCursor.pos())

    def add_new_type(self):
        """处理“添加新类别”按钮的点击事件。"""
        name, ok = QInputDialog.getText(self, "添加新类别", "请输入类别名称:")
        if not (ok and name): return

        # 1. 询问模型：名称是否重复？
        if self.model.is_name_duplicate(name):
            QMessageBox.warning(self, "操作失败", f"名称 '{name}' 已存在。")
            return

        color = QColorDialog.getColor(parent=self, title="为新类别选择颜色")
        if not color.isValid(): return

        # 2. 询问模型：颜色是否重复？
        if self.model.is_color_duplicate(color):
            QMessageBox.warning(self, "操作失败", f"颜色 '{color.name()}' 已被使用。")
            return

        # 3. 验证通过，创建并添加数据
        new_type = LabelTypeDataStruct(name, color)
        self.model.add_item(new_type)
        self.labelTypeAdded.emit(new_type.id)

    def edit_type(self, index: QModelIndex):
        """处理“编辑”操作。"""
        original_data = self.model.data(index, Qt.UserRole)
        if not original_data: return

        # 弹出对话框，预填充原始数据
        new_name, ok = QInputDialog.getText(self, "编辑类别", "请输入新名称:", text=original_data.label_type_name)
        if not (ok and new_name): return

        # 1. 询问模型：新名称是否与【其他项】重复？
        if self.model.is_name_duplicate(new_name, exclude_id=original_data.id):
            QMessageBox.warning(self, "操作失败", f"名称 '{new_name}' 已存在。")
            return

        new_color = QColorDialog.getColor(original_data.color, self, "选择新颜色")
        if not new_color.isValid(): return

        # 2. 询问模型：新颜色是否与【其他项】重复？
        if self.model.is_color_duplicate(new_color, exclude_id=original_data.id):
            QMessageBox.warning(self, "操作失败", f"颜色 '{new_color.name()}' 已被使用。")
            return

        # 3. 验证通过，更新模型
        update_dict = {"name": new_name, "color": new_color}
        self.model.setData(index, update_dict, Qt.EditRole)
        self.labelTypeUpdated.emit(original_data.id)

    def delete_type(self, index: QModelIndex):
        """处理“删除”操作。"""
        type_data = self.model.data(index, Qt.UserRole)
        if not type_data: return

        reply = QMessageBox.question(self, "删除确认", f"确定要删除类别 '{type_data.label_type_name}' 吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            type_id = type_data.id
            self.model.remove_item_by_row(index.row())
            self.labelTypeDeleted.emit(type_id)