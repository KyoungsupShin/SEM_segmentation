from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Keyboard_input():
    def keyPressEvent(self, e):
        #label 1 == "good" // 2 == 'defect' // 3 == 'etc'
        if e.key() == Qt.Key_Q:
            if self.label1 != 1:
                self.label1_ok_btn.setStyleSheet('background-color: green')
                self.label1_not_ok_btn.setStyleSheet('background-color: white')
                self.label1_etc_btn.setStyleSheet('background-color: white')
                self.label1 = 1  
                    
        elif e.key() == Qt.Key_W:
            if self.label2 != 1:
                self.label2_ok_btn.setStyleSheet('background-color: green')
                self.label2_not_ok_btn.setStyleSheet('background-color: white')
                self.label2_etc_btn.setStyleSheet('background-color: white')
                self.label2 = 1  

        elif e.key() == Qt.Key_E:
            if self.label3 != 1:
                self.label3_ok_btn.setStyleSheet('background-color: green')
                self.label3_not_ok_btn.setStyleSheet('background-color: white')
                self.label3_etc_btn.setStyleSheet('background-color: white')
                self.label3 = 1  
        
        elif e.key() == Qt.Key_A:
            if self.label1 != 2:
                self.label1_ok_btn.setStyleSheet('background-color: white')
                self.label1_not_ok_btn.setStyleSheet('background-color: green')
                self.label1_etc_btn.setStyleSheet('background-color: white')
                self.label1 = 2  

        elif e.key() == Qt.Key_S:
            if self.label2 != 2:
                self.label2_ok_btn.setStyleSheet('background-color: white')
                self.label2_not_ok_btn.setStyleSheet('background-color: green')
                self.label2_etc_btn.setStyleSheet('background-color: white')
                self.label2 = 2  

        elif e.key() == Qt.Key_D:
            if self.label3 != 2:
                self.label3_ok_btn.setStyleSheet('background-color: white')
                self.label3_not_ok_btn.setStyleSheet('background-color: green')
                self.label3_etc_btn.setStyleSheet('background-color: white')
                self.label3 = 2  

        elif e.key() == Qt.Key_Z:
            if self.label1 != 3:
                self.label1_ok_btn.setStyleSheet('background-color: white')
                self.label1_not_ok_btn.setStyleSheet('background-color: white')
                self.label1_etc_btn.setStyleSheet('background-color: green')
                self.label1 = 3  

        elif e.key() == Qt.Key_X:
            if self.label2 != 3:
                self.label2_ok_btn.setStyleSheet('background-color: white')
                self.label2_not_ok_btn.setStyleSheet('background-color: white')
                self.label2_etc_btn.setStyleSheet('background-color: green')
                self.label2 = 3  

        elif e.key() == Qt.Key_C:
            if self.label3 != 3:
                self.label3_ok_btn.setStyleSheet('background-color: white')
                self.label3_not_ok_btn.setStyleSheet('background-color: white')
                self.label3_etc_btn.setStyleSheet('background-color: green')
                self.label3 = 3  

        # elif e.key() == Qt.Key_Return:
        #     msg_option = QMessageBox.question(self, "SAVE Image", "이미지를 저장하시겠습니까?",QMessageBox.Yes | QMessageBox.Cancel)
        #     if msg_option == QtWidgets.QMessageBox.Yes:
        #         try:
        #             self.log_widget_prc.appendHtml(infoHtml2 + "{} 라벨링 되었습니다".format(self.cam2_cap_nam))
        #             self.hist_save_img.append(self.cam2_cap_nam)
        #             if len(self.hist_save_img) >= 10:
        #                 self.hist_save_img.pop(0)
        #             Global2.label = 0
        #             # Global2.label = True
        #         except:
        #             pass

        # elif e.key() == Qt.Key_K:
        #     #수동 캡처
        #     Global2.cap = True