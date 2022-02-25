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

class RECEIVER():
    def __init__(self):
        self.HOST = 'Localhost'
        self.PORT = 5555
        
    def Connect(self):        
        self.Receiver = socket(AF_INET, SOCK_STREAM)
        self.Receiver.bind((self.HOST, self.PORT))
        print('Receiver Socket binding {}'.format(self.Receiver))
        self.Receiver.listen(5)
        print('Receiver Listening')
    
    def Get_Tcp_mode(self):
        self.conn, self.addr = self.Receiver.accept()
        self.conn.settimeout(3)
        print('Connection accepted {}'.format(self.addr))
        self.health_check = self.conn.recv(1024).decode()
        if self.health_check == 'Health_check':
            self.conn.sendall('Alive'.encode())
        
    def Get_File_Info(self):        
        try:
            self.file_info = json.loads(self.conn.recv(4096).decode())    
            print('Json dumping done')
        except:
            print('Json dumping failed')
            self.Receiver.close()
            self.Connect()
            pass

    def Get_Result_Info(self):        
        # try:
        print('aaaaaaaaaaa')
        self.result_info = json.loads(self.conn.recv(1024).decode())    
        print(self.result_info)
        print('Result Json dumping done')
        # except:
        #     print('Result Json dumping failed')
        #     self.Receiver.close()
        #     self.Connect()
        #     pass

    def Get_File(self):
        data_transferred = 0
        data = self.file_info['file_length'] 

        self.conn.sendall('READY'.encode())
        print('Receiver ready to get a image')
        try:
            with open("../src/"+self.file_info['file_name'], 'wb') as f: 
                while True: 
                    data = self.conn.recv(1024)  
                    f.write(data) 
                    data_transferred += len(data)
                    if not data:
                        break
            print('Receiver got a image successfully')
        except:
            print('Receiver got a image failed')
            print(self.Receiver)
            self.Connect()
            pass

    def Get_result_data(self):
        self.file_result = json.loads(self.conn.recv(1024).decode())
        print(self.file_result)

class WB_Process():
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = int(PORT)
        self.connect()

    def connect(self):
        self.receiver = RECEIVER()
        self.receiver.HOST = self.HOST
        self.receiver.PORT = self.PORT        
        self.receiver.Connect()
        while True:            
            self.receiver.Get_Tcp_mode()
            if self.receiver.health_check != 'Health_check':
                self.receiver.Get_File_Info()
                self.receiver.Get_File()
                # self.receiver.Get_Result_Info()
        self.receiver.conn.close()

if __name__ == '__main__':
    wb = WB_Process(HOST = 'Localhost', PORT = 5555)

