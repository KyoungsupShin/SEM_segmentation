import sys
import os
import time
import cv2
import numpy as np
import datetime
import copy
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import glob 
from socket import *
import json 
import sys
sys.path.append('./utils')
from Sender import * 
# from apc_log import *
# log = APC_Log('Thread', propagate=False)
font = cv2.FONT_HERSHEY_PLAIN

class Global(object):
    image_path = None
    read_mode = None
    img_number = 0
    tcp_conn = False
    send_tcp = False
    tcp_cancel = False
    health_tcp = False
    tcp_idle = False
    save_result_img = False
    save_result_data = False
    setting_model_thres = 0
    setting_model_config1 = True
    binary_image_mode = False

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    changePixmap2 = pyqtSignal(QImage)
    networksignal = pyqtSignal(str)

    def run(self): 
        if Global.read_mode is not None:
            if Global.read_mode == 'image':
                img = cv2.imread(Global.image_path)
                p = self.image_send(img)
                self.changePixmap.emit(p)     
            if Global.read_mode == 'directory':
                img_list = glob.glob(str(Global.image_path) + '/*.jpg')
                img = cv2.imread(img_list[Global.img_number])
                p = self.image_send(img)
                self.changePixmap.emit(p)     
    
            if Global.send_tcp == True:
                self.sender = SENDER(HOST = '172.23.69.100', PORT = 5555, processing = True)
                img_name = Global.image_path.split('/')[-1]
                self.sender.main(base_path = Global.image_path, img_name = img_name)
                self.networksignal.emit('이미지 전송 성공')
                img = cv2.imread(self.sender.result_path)
                p = self.image_send(img)
                self.changePixmap2.emit(p)     
                Global.send_tcp = False

            if Global.binary_image_mode == True:
                img = cv2.imread('./tmp/test2.jpg')
                p = self.image_send(img)
                self.changePixmap2.emit(p)     

            if Global.binary_image_mode == False:
                try:
                    img = cv2.imread(self.sender.result_path)
                    p = self.image_send(img)
                    self.changePixmap2.emit(p)     
                except:
                    pass

            if Global.save_result_data == True:
                try:
                    df = pd.DataFrame.from_dict(self.sender.file_info)
                    df.to_csv('result.csv')
                    self.networksignal.emit('결과 데이터 저장')
                    Global.save_result_data = False
                except:
                    Global.save_result_data = False
                    pass
                    
        
        if Global.tcp_conn == True:
            self.networksignal.emit('TCP 통신 접속 시도 중....')
            self.sender = SENDER(HOST = '172.23.69.100', PORT = 5555)
            if self.sender.connected == True:
                self.networksignal.emit('TCP 통신 접속 성공')
            else:
                self.networksignal.emit('TCP 통신 접속 실패')
            Global.tcp_conn = False

        if Global.tcp_cancel == True:
            try:
                self.sender.Sender.close()
                self.networksignal.emit('TCP 통신 종료')
            except:
                self.networksignal.emit('TCP 통신 없음')
            Global.tcp_cancel = False


        if Global.health_tcp == True:
            self.sender = SENDER(HOST = '172.23.69.100', PORT = 5555, send_check = True)
            self.networksignal.emit("통신 체크: {}".format(self.sender.health_check_result))
            if self.sender.health_check_result == 'Alive':
                self.networksignal.emit('TCP 통신 상태 양호')
            else:
                self.networksignal.emit('TCP 통신 상태 불량')
            Global.health_tcp = False

        if Global.tcp_idle == True:
            self.sender = SENDER(HOST = '172.23.69.100', PORT = 5555, idle = True)
            self.networksignal.emit('프로세스 서버 IDLE')
            Global.tcp_idle = False

    def image_send(self, img):
        try:
            h, w, ch = img.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(820, 720, Qt.KeepAspectRatio)
            return p
        except:
            pass

    def stop(self):
        self.isRun = False
        self.wait()


