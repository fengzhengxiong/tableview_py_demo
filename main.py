#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：main.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 15:58 
'''


# main.py
import sys
import random

from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar, QDockWidget, QTabWidget, QWidget
from PySide6.QtCore import Qt

from managers.FileManager import FileManager
from managers.ImageInfoManager import ImageInfoManager
from managers.LabelInfoManager import LabelInfoManager
from managers.LabelTypeManager import LabelTypeManager

from data.TableDataStruct import ImageInfoDataStruct, LabelInfoDataStruct


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("大型工业软件 - 重构模块")
        self.setGeometry(100, 100, 1600, 900)

        self.create_managers()
        self.setup_ui()
        self.connect_signals()

    def create_managers(self):
        self.file_manager = FileManager(self)
        self.image_info_manager = ImageInfoManager(self)
        self.label_info_manager = LabelInfoManager(self)
        self.label_type_manager = LabelTypeManager(self)

    def setup_ui(self):
        self.setCentralWidget(QWidget())  # 中央控件可以是一个图像查看器等

        file_dock = QDockWidget("文件列表", self)
        file_dock.setWidget(self.file_manager)
        self.addDockWidget(Qt.LeftDockWidgetArea, file_dock)

        right_dock = QDockWidget("信息与标签", self)
        tab_widget = QTabWidget()
        tab_widget.addTab(self.image_info_manager, "图片基础信息")
        tab_widget.addTab(self.label_info_manager, "标签列表")
        tab_widget.addTab(self.label_type_manager, "标签类别")
        right_dock.setWidget(tab_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, right_dock)

        self.setStatusBar(QStatusBar(self))

    def connect_signals(self):
        self.file_manager.view.selectionModel().selectionChanged.connect(self.on_file_selection_changed)
        self.file_manager.deleteFileItemEmit.connect(self.on_file_deleted)
        self.file_manager.topButtonClicked.connect(self.on_main_action)
        self.label_info_manager.visibilityChanged.connect(
            lambda lid, vis: self.statusBar().showMessage(f"标签 {lid[:8]}... 可见性: {vis}", 3000)
        )
        self.label_type_manager.labelTypeAdded.connect(
            lambda id: self.statusBar().showMessage(f"已添加类别: {id}", 3000)
        )

    def on_file_selection_changed(self, selected, deselected):
        # 获取选中的代理索引
        indexes = self.file_manager.view.selectionModel().selectedRows()
        if not indexes:
            self.label_info_manager.clear_labels()
            self.image_info_manager.clear_info()
            return

        # --- 关键修正 ---
        # 1. 获取到的是代理模型的索引 (Proxy Index)
        proxy_index = indexes[0]

        # 2. 将代理索引映射到源模型索引 (Source Index)
        source_index = self.file_manager.proxy_model.mapToSource(proxy_index)

        # 3. 使用源索引从源模型获取数据
        file_data = self.file_manager.source_model.data(source_index, Qt.UserRole)
        # --- 修正结束 ---

        if file_data:
            # 伪造数据进行演示
            dummy_labels = [LabelInfoDataStruct(f"label_{i}", random.choice(["person", "car"])) for i in
                            range(random.randint(1, 5))]
            dummy_info = ImageInfoDataStruct(file_data.file_image_name, "常规项目", "1920x1080")

            self.label_info_manager.set_labels(dummy_labels)
            self.image_info_manager.display_info(dummy_info)

    def on_file_deleted(self, file_ids: list):
        message = f"文件已删除: {file_ids[0][:8]}..." if len(file_ids) == 1 else f"已删除 {len(file_ids)} 个文件。"
        self.statusBar().showMessage(message, 5000)
        print(message)

    def on_main_action(self, action_name: str):
        message = f"接收到顶层操作: {action_name}"
        self.statusBar().showMessage(message, 3000)
        print(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())