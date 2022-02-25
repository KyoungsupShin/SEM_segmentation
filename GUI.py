import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
import datetime
import time
import glob
import numpy as np
import keyboard  
from log import *
sys.path.append('./threading')
sys.path.append('./utils')
from thread1 import * 
from setting import * 
log = APC_Log('GUI')
'''
기능1: 이미지 실시간 렌더링
기능2: 이미지 실시간 캡처 통신
기능3: APC서버 통신 상태 확인
기능4: PLC 통신 상태 확인
'''
class Maindisplay(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1200, 1000)
        self.setWindowTitle("Hanwha Qcells J-BOX detection 1.0")
        self.window_layout = QGridLayout()
        self.initUI()

    def initUI(self):     
        self.Menubar() #MENU BAR
        self.Commend_Process() #PUSH BUTTON
        self.Command_process_events()
        self.VideoBox() #VIDEO BOX
        self.Processing_Log() #PROCESS LOG BOX
        self.Image_reading()
        # self.Connection_status() #CONNECTION LED BOX

        centralWidget = QWidget()
        centralWidget.setLayout(self.window_layout)
        self.setCentralWidget(centralWidget)

    def Menubar(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('INFO')
        openMenu = QAction(QIcon("Icon.png"), "version", self)
        fileMenu.addAction(openMenu)
        #openMenu.triggered.connect(self.SubWindow_onButtonClicked)
        self.show()

    def Commend_Process(self):
        self.process_commend_layout = QGridLayout()
        self.process_commend_layout2 = QGridLayout()

        groupBox = QGroupBox('실행 박스', self)
        groupBox2 = QGroupBox('이미지 이동', self)

        self.image_path_btn = QPushButton('이미지 불러오기')
        self.image_dir_path_btn = QPushButton('폴더 불러오기')
        self.server_call_btn = QPushButton('통신 시작')
        self.image_send_btn = QPushButton('이미지 통신')
        self.server_cancel_btn = QPushButton('통신 종료')
        self.tcp_health_check_btn = QPushButton('통신 체크')
        self.server_idle_btn = QPushButton('대기 모드')
        self.setting_seg_btn = QPushButton('모델 설정')
        self.image_save_btn = QPushButton('결과 이미지 저장')
        self.result_save_btn = QPushButton('결과 데이터 저장')

        self.pre_img_btn = QPushButton('◀◀◀')
        self.next_img_btn = QPushButton('▶▶▶')

        self.process_commend_layout.addWidget(self.image_path_btn, 0, 0)
        self.process_commend_layout.addWidget(self.image_dir_path_btn, 0, 1)   
        self.process_commend_layout.addWidget(self.server_call_btn, 1, 0)   
        self.process_commend_layout.addWidget(self.image_send_btn, 1, 1)
        self.process_commend_layout.addWidget(self.server_cancel_btn, 2, 0)
        self.process_commend_layout.addWidget(self.tcp_health_check_btn, 2, 1)
        self.process_commend_layout.addWidget(self.server_idle_btn, 3, 0)
        self.process_commend_layout.addWidget(self.setting_seg_btn, 3, 1)
        self.process_commend_layout.addWidget(self.image_save_btn, 4, 0)   
        self.process_commend_layout.addWidget(self.result_save_btn, 4, 1)

        self.process_commend_layout2.addWidget(self.pre_img_btn, 0, 0)
        self.process_commend_layout2.addWidget(self.next_img_btn, 0, 1)

        groupBox.setLayout(self.process_commend_layout)
        groupBox2.setLayout(self.process_commend_layout2)

        self.window_layout.addWidget(groupBox, 0, 0) 
        self.window_layout.addWidget(groupBox2, 1, 0) 

    def Command_process_events(self):
        self.image_path_btn.clicked.connect(self.File_dialog_path)
        self.image_dir_path_btn.clicked.connect(self.Folder_dialog_path)
        self.pre_img_btn.clicked.connect(self.Slide_img)
        self.next_img_btn.clicked.connect(self.Slide_img)
        self.server_call_btn.clicked.connect(self.Tcp_conn)
        self.image_send_btn.clicked.connect(self.Tcp_image_send)
        self.server_cancel_btn.clicked.connect(self.Tcp_cancel)
        self.tcp_health_check_btn.clicked.connect(self.Tcp_health_check)
        self.server_idle_btn.clicked.connect(self.Tcp_idle)
        self.setting_seg_btn.clicked.connect(self.Setting_seg)
        self.image_save_btn.clicked.connect(self.Save_result_img)
        self.result_save_btn.clicked.connect(self.Save_result_to_csv)
                
    def Show_thread_image(self):
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        self.show()

    def Show_thread_result_image(self):
        self.th.changePixmap2.connect(self.setImage2)
        self.th.start()
        self.show()

    def File_dialog_path(self):
        Global.read_mode = 'image'
        fname = QFileDialog.getOpenFileName(self)
        Global.image_path = fname[0] 
        self.Show_thread_image()
        
    def Folder_dialog_path(self):
        Global.read_mode = 'directory'
        fname = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        Global.image_path = fname
        self.Show_thread_image()

    def Slide_img(self):
        Global.img_number = Global.img_number + 1 
        self.Show_thread_image()

    def Tcp_conn(self):
        Global.tcp_conn = True
        self.th.start()

    def Tcp_image_send(self):
        Global.send_tcp = True
        # self.th.start()
        self.Show_thread_result_image()

    def Tcp_cancel(self):
        Global.tcp_cancel = True
        self.th.start()

    def Tcp_health_check(self):
        Global.health_tcp = True
        self.th.start()

    def Tcp_idle(self):
        Global.tcp_idle = True
        self.th.start()

    def Setting_seg(self):
        win = SubWindow()
        r = win.showModal()
        return 0 

    def Save_result_img(self):
        Global.save_result_img = True
        self.th.start()
        
    def Save_result_to_csv(self):
        Global.save_result_data = True
        self.th.start()

    def Change_binary(self):
        if Global.binary_image_mode == False:   
            Global.binary_image_mode = True
        else:
            Global.binary_image_mode = False
        self.th.start()

    def VideoBox(self):
        self.VideoBox_Layout_Main = QHBoxLayout()
        self.VideoBox_Layout_sub1 = QGridLayout()                
        self.VideoBox_Layout_sub2 = QGridLayout()                

        groupBox = QGroupBox('SEM IMAGE', self)

        self.VideoBox_label = QLabel(self) #Main Video
        self.VideoBox_label_name = QLabel(self, text = 'ORIGIN IMAGE') #Main Video
        self.VideoBox_label.setFixedSize(820, 620)    
        self.VideoBox_label.setStyleSheet("border: 1px solid black;")

        self.VideoBox_label2 = QLabel(self) #Main Video
        self.VideoBox_label2_name = QLabel(self, text = 'SEGMENTIC IMAGE') #Main Video
        self.VIdeoBox_label2_change  = QPushButton('BINARAY')
        self.VIdeoBox_label2_change.clicked.connect(self.Change_binary)
        self.VideoBox_label2.setFixedSize(820, 620)    
        self.VideoBox_label2.setStyleSheet("border: 1px solid black;")

        self.VideoBox_Layout_sub1.addWidget(self.VideoBox_label_name,0,0)
        self.VideoBox_Layout_sub1.addWidget(self.VideoBox_label,1,0, 1, 3)
        self.VideoBox_Layout_Main.addLayout(self.VideoBox_Layout_sub1)

        self.VideoBox_Layout_sub2.addWidget(self.VideoBox_label2_name,0,0)
        self.VideoBox_Layout_sub2.addWidget(self.VIdeoBox_label2_change, 0, 1)   
        self.VideoBox_Layout_sub2.addWidget(self.VideoBox_label2,1,0, 1, 3)
        self.VideoBox_Layout_Main.addLayout(self.VideoBox_Layout_sub2)

        groupBox.setLayout(self.VideoBox_Layout_Main)
        self.window_layout.addWidget(groupBox, 0, 1) 

    def Processing_Log(self):
        self.process_log_layout = QGridLayout()

        groupBox = QGroupBox('분석 로그', self)

        self.log_widget_prc = QPlainTextEdit(self)
        self.log_widget_prc_name = QLabel(self, text = 'PROCESS Logs') #Main Video
        self.log_widget_prc.setReadOnly(True)
        self.log_widget_prc.appendPlainText('=' * 5 + 'Process Logs' + '=' * 5)

        self.log_widget_conn = QPlainTextEdit(self)
        self.log_widget_conn_name = QLabel(self, text = 'NETWORK Logs') #Main Video
        self.log_widget_conn.setReadOnly(True)
        self.log_widget_conn.appendPlainText('=' * 5 + 'Connection Logs' + '=' * 5)

        self.process_log_layout.addWidget(self.log_widget_prc_name, 0, 0)
        self.process_log_layout.addWidget(self.log_widget_conn_name, 0, 1)        
        self.process_log_layout.addWidget(self.log_widget_prc, 1, 0)
        self.process_log_layout.addWidget(self.log_widget_conn, 1, 1)

        groupBox.setLayout(self.process_log_layout)
        self.window_layout.addWidget(groupBox, 1, 1) 

    def Image_reading(self):
        self.th = Thread(self)
        self.th.networksignal.connect(self.setString)
    
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.VideoBox_label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def setImage2(self, image):
        self.VideoBox_label2.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def setString(self, msg):
        self.log_widget_conn.appendHtml(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Maindisplay()
    w.show()
    sys.exit(app.exec_())

