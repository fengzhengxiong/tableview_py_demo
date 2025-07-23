Demo 开发介绍：
---
## 开发背景：
阿熊开发了一款软件，其中用到了tableWidget，但是在发布了几个版本之后，越发觉得tableWidget局限性太大：
- 1：数据过多的时候，会导致界面卡顿，多线程也解决不了
- 2：插入，删除，更新等操作，越发的占据资源
- 3：对其多行选中并操作，可操作性差

遂开发了这款demo

demo 用view-model-delegates的格式，插入删除，多线程等都有涉及。
性能较之前有很大的优化。

---
## 项目环境：
- python = 3.13.5

- colorama = 0.4.6
- lxml = 6.0.0
- numpy = 2.2.6
- opencv-python = 4.12.0.88
- pillow = 11.3.0
- pip = 25.1
- psutil = 7.0.0
- PySide6 = 6.9.1
- PySide6_Addons = 6.9.1
- PySide6_Essentials = 6.9.1
- PyYAML = 6.0.2
- setuptools = 78.1.1
- shiboken6 = 6.9.1
- tqdm = 4.67.1
- wheel = 0.45.1

---
## 开发目的：
- 学习一种高效率的架构模式。
- 不再受限于QTableWidget这个垃圾控件。