#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：FileManager.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:08 
'''

# managers/FileManager.py

import random
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox, QMenu
from PySide6.QtCore import Signal, QModelIndex, Qt, QTimer, QThread, Slot
from PySide6.QtGui import QColor, QCursor

from workers.FilterWorker import FilterWorker
from models.FileFilterProxyModel import FileFilterProxyModel
from models.FileTableModel import FileTableModel, COL_OP
from views.BaseTableView import BaseTableView
from delegates.CustomDelegate import CustomDelegate
from data.TableDataStruct import FileDataStruct, train_color, val_color

STATE_CONFIG = {
    "训练集": {"text": "转为训练集", "color": train_color},
    "验证集": {"text": "转为验证集", "color": val_color},
}


class FileManager(QWidget):
    deleteFileItemEmit = Signal(list)
    updateFileStateEmit = Signal(str, str)
    topButtonClicked = Signal(str)
    filter_requested = Signal(list, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # --- 新增：创建防抖定时器 ---
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)  # 设置为单次触发
        self.search_timer.setInterval(300)  # 设置延迟时间，300ms是一个不错的选择

        self._init_model_view()
        self._init_background_worker()  # 初始化后台线程
        self._init_ui()
        self._connect_signals()
        self._add_test_data(10000)

    def _init_model_view(self):
        headers = ["序号", "文件名称", "文件类别", "操作"]

        # 1. 创建源模型 (Source Model)
        self.source_model = FileTableModel(headers=headers)

        # 2. 创建代理模型 (Proxy Model)
        self.proxy_model = FileFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.source_model)

        # 3. 视图连接到代理模型
        self.view = BaseTableView(column_width_ratios=[1, 4, 4, 1])
        self.view.setModel(self.proxy_model)  # <-- 关键改变

        self.delegate = CustomDelegate(self)
        # 注意：在代理模型下，列号保持不变
        self.view.setItemDelegateForColumn(COL_OP, self.delegate)

    def _init_background_worker(self):
        """设置后台线程和工作者对象。"""
        self.filter_thread = QThread()
        self.filter_worker = FilterWorker()
        self.filter_worker.moveToThread(self.filter_thread)
        self.filter_thread.start()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        top_button_layout = QHBoxLayout()
        self.btn_import_img = QPushButton("导入图片")
        self.btn_import_img.setObjectName("import_image")
        self.btn_import_dataset = QPushButton("导入数据集")
        self.btn_import_dataset.setObjectName("import_dataset")
        self.btn_export_dataset = QPushButton("导出数据集")
        self.btn_export_dataset.setObjectName("export_dataset")
        self.btn_generate_dataset = QPushButton("生成数据集")
        self.btn_generate_dataset.setObjectName("generate_dataset")
        self.btn_auto_label = QPushButton("预标注")
        self.btn_auto_label.setObjectName("auto_label")

        self.top_buttons = [
            self.btn_import_img,
            self.btn_import_dataset,
            self.btn_export_dataset,
            self.btn_generate_dataset,
            self.btn_auto_label
        ]
        for btn in self.top_buttons: top_button_layout.addWidget(btn)
        main_layout.addLayout(top_button_layout)

        control_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("按文件名查找 (后台筛选)...")
        self.add_10000_button = QPushButton("添加10000个文件 (测试)")
        control_layout.addWidget(self.search_bar)
        control_layout.addWidget(self.add_10000_button)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.view)
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)

    def _connect_signals(self):
        # 防抖定时器连接到启动后台任务的槽
        self.search_timer.timeout.connect(self.start_background_filter)
        self.search_bar.textChanged.connect(self.search_timer.start)

        # 连接主线程和后台线程
        self.filter_requested.connect(self.filter_worker.run_filter)
        self.filter_worker.results_ready.connect(self.update_proxy_with_results)

        self.view.clicked.connect(self.on_view_clicked)
        self.view.customContextMenuRequested.connect(self.show_context_menu)
        for btn in self.top_buttons:
            btn.clicked.connect(lambda checked=False, name=btn.objectName(): self.topButtonClicked.emit(name))
        self.add_10000_button.clicked.connect(lambda: self._add_test_data(10000))

    def start_background_filter(self):
        """由防抖定时器触发，准备数据并发起后台过滤请求。"""
        search_text = self.search_bar.text()

        if not search_text:
            # 如果搜索框为空，直接重置过滤器，无需动用后台线程
            self.proxy_model.set_accepted_rows(None)
            return

        # 将整个数据列表和搜索文本通过信号发送给工作者
        # 注意：这里传递的是数据的引用，因为后台是只读的，这样更高效
        # 如果后台需要修改数据，必须传递深拷贝！
        self.filter_requested.emit(self.source_model._data, search_text)

        # 可以在这里添加一个"正在搜索..."的UI提示
        self.search_bar.setStyleSheet("background-color: #fffde7;")  # 淡黄色背景提示

    @Slot(set)
    def update_proxy_with_results(self, accepted_rows: set):
        """接收后台线程的结果，并更新代理模型。"""
        self.view.setUpdatesEnabled(False)
        self.proxy_model.set_accepted_rows(accepted_rows)
        self.view.setUpdatesEnabled(True)

        # 恢复UI提示
        self.search_bar.setStyleSheet("")

    def closeEvent(self, event):
        """确保在关闭窗口时，后台线程能被安全地停止。"""
        self.filter_thread.quit()
        self.filter_thread.wait()
        super().closeEvent(event)

    # --- 新增的槽函数 ---
    def _add_test_data(self, count: int):
        # 注意：现在数据被添加到源模型中
        print(f"Adding {count} items to FileManager...")
        states = ["未标注", "已标注", "训练集", "验证集"]
        for i in range(count):
            file_name = f"image_{self.source_model.rowCount() + 1:04d}.jpg"
            state = random.choice(states)
            color = train_color if state == "训练集" else val_color if state == "验证集" else QColor("black")
            # 添加到源模型
            self.source_model.add_item(FileDataStruct(file_name, state, color))
        print("Done.")

    # --- 新增的槽函数 ---

    def on_view_clicked(self, index: QModelIndex):
        if not index.isValid(): return
        # 获取源模型的索引，以便后续操作
        source_index = self.proxy_model.mapToSource(index)
        if source_index.column() == COL_OP:
            # 传递源模型的行号进行删除
            self._confirm_and_delete_files([source_index.row()])

    def show_context_menu(self, position):
        # 不需要修改，因为后续的操作会基于 selectionModel
        if not self.view.selectionModel().hasSelection(): return
        menu = QMenu(self.view)
        for state_name, config in STATE_CONFIG.items():
            action = menu.addAction(config["text"])
            action.triggered.connect(
                lambda c=False, s=state_name, cl=config["color"]: self.change_selected_files_state(s, cl))
        menu.addSeparator()
        delete_action = menu.addAction("删除")
        delete_action.triggered.connect(self.delete_selected_files)
        menu.exec(QCursor.pos())

    def change_selected_files_state(self, new_state: str, new_color: QColor):
        selected_indexes = self.view.selectionModel().selectedRows()
        for proxy_index in selected_indexes:
            # 将代理索引映射回源索引
            source_index = self.proxy_model.mapToSource(proxy_index)
            # 对源模型进行操作
            self.source_model.update_item_state(source_index.row(), new_state, new_color)
            file_data = self.source_model.get_item_by_row(source_index.row())
            if file_data:
                self.updateFileStateEmit.emit(file_data.id, new_state)

    def delete_selected_files(self):
        selected_proxy_indexes = self.view.selectionModel().selectedRows()
        # 将代理行号列表转换为源行号列表
        source_rows_to_delete = [self.proxy_model.mapToSource(idx).row() for idx in selected_proxy_indexes]
        self._confirm_and_delete_files(source_rows_to_delete)

    def _confirm_and_delete_files(self, source_rows: list):
        # 这个函数现在接收的是源模型的行号列表，逻辑无需大改
        if not source_rows: return
        message = (f"确定要删除文件 '{self.source_model.get_item_by_row(source_rows[0]).file_image_name}' 吗？" if len(
            source_rows) == 1
                   else f"确定要删除选中的 {len(source_rows)} 个文件吗？")
        if QMessageBox.question(self, "删除确认", message, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            ids_to_delete = [self.source_model.get_item_by_row(row).id for row in source_rows]
            # 对源模型进行删除操作
            for row in sorted(source_rows, reverse=True):
                self.source_model.remove_item_by_row(row)
            if ids_to_delete: self.deleteFileItemEmit.emit(ids_to_delete)