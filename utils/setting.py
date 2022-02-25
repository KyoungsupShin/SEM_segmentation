from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SubWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('모델 설정')
        self.setGeometry(0, 0, 400, 600)
        self.window_layout = QGridLayout()
        self.Command_btn()

    def Command_btn(self):
        self.process_commend_layout = QGridLayout()
        groupBox = QGroupBox('세팅 박스', self)

        self.save_values_btn = QPushButton('저장')
        self.cancel_btn = QPushButton('취소')

        self.process_commend_layout.addWidget(self.save_values_btn, 0, 0)
        self.process_commend_layout.addWidget(self.cancel_btn, 0, 1)  

        groupBox.setLayout(self.process_commend_layout)
        self.window_layout.addWidget(groupBox, 0, 0) 

    def Json_setting(self):
        #threshold, max_num_obj, resize
        pass

    def Save_setting(self):
        pass

    def showModal(self):
       return super().exec_()