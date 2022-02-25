from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def get_selected_calender(self):
    self.start_time = self.calender.selectedDate().toString("yyyyMMdd")
    end_time = datetime.datetime.strptime(self.start_time, "%Y%m%d") + datetime.timedelta(days=1)
    self.end_time = end_time.strftime('%Y%m%d')
    self.calender_select_start_date.setText("시작날짜: " + self.start_time)
    self.calender_select_end_date.setText("종료날짜: " + self.end_time)