#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Project ：tableview_py_demo 
@File    ：FilterWorker.py
@Author  ：fengzhengxiong
@Date    ：2025/7/23 16:11 
'''

# workers/FilterWorker.py (新文件)

from PySide6.QtCore import QObject, Signal, Slot
from data.TableDataStruct import FileDataStruct


class FilterWorker(QObject):
    """
    在后台线程中运行的过滤器工作者。
    """
    # 信号：当过滤完成时发射，参数是匹配项的源模型行号集合
    results_ready = Signal(set)

    @Slot(list, str)
    def run_filter(self, source_data: list[FileDataStruct], search_text: str):
        """
        接收数据和搜索文本，在后台执行过滤。
        """
        search_text_lower = search_text.lower()
        accepted_rows = set()

        # 这是在后台线程中执行的耗时循环
        for i, item_data in enumerate(source_data):
            if search_text_lower in item_data.file_image_name.lower():
                accepted_rows.add(i)

        # 发射信号，将结果传回主线程
        self.results_ready.emit(accepted_rows)