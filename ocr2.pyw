# -*- coding: utf-8 -*-

"""
ﾏﾙﾁﾓﾆﾀの全画面から選択してｽｸﾘｰﾝｼｮｯﾄ&画像の文字読み取り
ｸﾘｯﾌﾟﾎﾞｰﾄﾞに送る
"""

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from PIL import ImageGrab, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pyautogui
import re

#範囲ｸﾛｯﾌﾟ後に呼ばれる処理
def imgtotxt(img):
	import pyocr
	import pyperclip
	import re
	import os
	import sys

	import clipc
	
	path="C:\Program Files\Tesseract-OCR"
	if path not in os.environ["PATH"].split(os.pathsep):
		os.environ["PATH"] += os.pathsep + path

	tools = pyocr.get_available_tools() 
	if len(tools) == 0:
		print("OCRエンジンが指定されていません")
		sys.exit(1)
	else:
		tool = tools[0]

	builder = pyocr.builders.TextBuilder(tesseract_layout=6)
	try:
		result = tool.image_to_string(img,lang="jpn",builder=builder)
		pyperclip.copy(clipc.change(result))
	except Exception as e:
		print("error!")
		print(e)
	#pyperclip.copy(result.strip())
	#clipc.change()
	

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk( screenName=r'\\\\.\\DISPLAY1')
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(-screen_width,0,screen_width*2, screen_height)
        self.setWindowTitle("")
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        print("Capture the screen...")
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor("black"), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))       

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = getscr()
        img = img.crop((x1,y1,x2,y2))

        imgtotxt(img)

def getscr():
	#ｻﾌﾞﾓﾆﾀｰも含めたｽｸﾘｰﾝｼｮｯﾄ
	#https://funmatu.wordpress.com/2017/06/01/pyautogui%EF%BC%9Fpywinauto%EF%BC%9F/
	#https://stackoverflow.com/questions/6951557/pil-and-bitmap-from-winapi
	import win32gui
	import win32api
	import win32ui
	import win32con

	from PIL import Image
	 
	hwnd = win32gui.GetDesktopWindow()
	 
	# get complete virtual screen including all monitors
	SM_XVIRTUALSCREEN = 76
	SM_YVIRTUALSCREEN = 77
	SM_CXVIRTUALSCREEN = 78
	SM_CYVIRTUALSCREEN = 79
	w = vscreenwidth = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
	h = vscreenheigth = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
	l = vscreenx = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
	t = vscreeny = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)
	r = l + w
	b = t + h
	 
	hwndDC = win32gui.GetWindowDC(hwnd)
	mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
	saveDC = mfcDC.CreateCompatibleDC()
	 
	saveBitMap = win32ui.CreateBitmap()
	saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
	saveDC.SelectObject(saveBitMap)
	saveDC.BitBlt((0, 0), (w, h),  mfcDC,  (l, t),  win32con.SRCCOPY)

	bmpinfo = saveBitMap.GetInfo()
	bmpstr = saveBitMap.GetBitmapBits(True)
	img = Image.frombuffer(
		'RGB',
		(bmpinfo['bmWidth'], bmpinfo['bmHeight']),
		bmpstr, 'raw', 'BGRX', 0, 1)

	return img

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())


