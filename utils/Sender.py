import sys
# from apc_log import APC_Log
from socket import *
import json 
import cv2
import os
import time
import shutil
import datetime
import numpy as np

class SENDER():
    def __init__(self, HOST, PORT, processing = False, send_check = False, idle = False):
        self.HOST = HOST
        self.PORT = PORT
        self.sender_list = []
        self.processing = processing
        self.send_check = send_check
        self.idle = idle 
        self.health_check_result = 'died'
        self.status = 'Not working'
        self.Connect()
        
    def Connect(self):
        cnt = 0
        self.connected = False
        if len(self.sender_list) >= 2:
            for i in self.sender_list:
                i[0].close()
        try:
            self.Sender = socket(AF_INET, SOCK_STREAM)
            self.Sender.settimeout(1)
            self.Sender.connect((self.HOST, self.PORT))
            self.connected = True
        except:
            while self.connected == False:
                time.sleep(1)
                try:
                    cnt = cnt + 1
                    print("TCP 연결 시도 중 ... COUNT: {}".format(cnt))
                    if cnt >= 3:
                        break                   
                    self.Sender = socket(AF_INET, SOCK_STREAM)
                    self.Sender.settimeout(1)
                    self.Sender.connect((self.HOST, self.PORT))
                    self.connected = True
                    break
                except:
                    pass
            self.connected = False
            pass

        self.sender_list.append([self.Sender])
        if self.processing == True:
            self.Processing()
        elif self.send_check == True:
            self.Health_check()
        elif self.idle == True:
            self.Idle()
        else:
            self.Just_conn()

    def Just_conn(self):
        try:
            self.Sender.sendall('connect'.encode())
            if self.Sender.recv(1024).decode() == 'connected':
                self.status = 'connected'
            else:
                self.status = 'unconnected'
        except:
            pass

    def Processing(self):
        try:
            if self.processing == True:
                self.Sender.sendall('processing'.encode())
                if self.Sender.recv(1024).decode() == 'Working':
                    self.status = 'Working'
                else:
                    self.status = 'Not working'
            else:
                pass
        except:
            pass

    def Idle(self):
        try:
            if self.idle == True:
                self.Sender.sendall('Make Idle'.encode())
                if self.Sender.recv(1024).decode() == 'Done':
                    self.status = 'Idle'
                else:
                    self.status = 'Working'
            else:
                pass
        except:
            pass

    def Health_check(self):
        try:
            if self.send_check == True:
                self.Sender.sendall('Health_check'.encode())
                if self.Sender.recv(1024).decode() == 'Alive':
                    self.health_check_result = 'Alive'
            else:
                self.Sender.sendall('Health_check_pass'.encode())
        except:
            self.health_check_result = 'died'
            pass

    def Dump_Json(self, base_path, img_name):
        file_info = {
                    'file_name' : img_name,
                    'file_length' : self.GetFileSize(base_path),
                    'create_time' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
        send_data = json.dumps(file_info)
        self.Sender.send(send_data.encode())
        time.sleep(0.05)

    def GetFileSize(self, base_path):        
        filesize = os.path.getsize(base_path)
        return str(filesize)

    def GetFileData(self, base_path):
        data_transferred = 0
        with open(base_path, 'rb') as f:
            data = f.read(1024)
            while data:
                data_transferred += self.Sender.send(data)
                data = f.read(1024)
        
        # os.remove(self.base_path)
        # time.sleep(0.05)

    def Get_File_Info(self):        
        try:
            self.file_info = json.loads(self.Sender.recv(4096).decode())    
            print('Json dumping done')
            print(self.file_info)
        except:
            print('Json dumping failed')
            self.Sender.close()
            self.Connect()
            pass

    def Get_File_reverse(self):
        data_transferred = 0
        data = self.file_info['file_reverse_length'] 
        self.Sender.settimeout(1)
        try:
            with open("./tmp/"+self.file_info['file_reverse_name'], 'wb') as f: 
                while True: 
                    data = self.Sender.recv(1024)  
                    f.write(data) 
                    data_transferred += len(data)
                    if not data:
                        break
        except:
            print('Receiver got a image successfully')
            pass    

    def Get_File(self):
        data_transferred = 0
        data = self.file_info['file_length'] 
        self.Sender.sendall('READY'.encode())
        self.result_path = "./tmp/"+self.file_info['file_name']
        
        self.Sender.settimeout(1)
        try:
            with open("./tmp/"+self.file_info['file_name'], 'wb') as f: 
                while True: 
                    data = self.Sender.recv(1024)  
                    f.write(data) 
                    data_transferred += len(data)
                    if not data:
                        break
        except:
            print('Receiver got a image successfully')
            pass    


    def main(self, base_path, img_name):
        try:
            self.Dump_Json(base_path, img_name) #이미지 정보 송신
            status = self.Sender.recv(1024) #이미지 송신 상태 
            if status.decode() == 'READY': 
                time.sleep(0.1)
                self.GetFileData(base_path) #이미지 전송
                
            self.Sender.settimeout(10)
            status = self.Sender.recv(1024) #이미지 송신 상태
            if status.decode() == 'READY':
                self.Get_File_Info()
                self.Get_File()
                time.sleep(0.1)
                self.Sender.sendall('READY'.encode())
                self.Get_File_reverse()

            print(self.result_path)
            self.Sender.close()
            return 'True'
        except:
            return 'False'
            pass