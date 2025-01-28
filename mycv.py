import sys
import math
import itertools

import cv2
import numpy as np
import win32gui

def main():
	Visualize(Draw)

class Draw:
#Visualizeの属性
#窓の名前name / 背景画像base_img / 描画画像step_img / 表示間隔wait
	def __init__(self,frame):#base_imgに元となる画像を入れる
		frame.wait = 0
		frame.base_img = Img("").grid(10*6,16*6,(100,100,100))
		
	def main(self,frame):#step_img(base_imgの複製)の描画を記述する
		pass

class Img:#画像データ全体の編集
	def __init__(self,img):
		def _makeimg(size):
		#指定sizeのnp配列を返す(黒のみ画像)
			width,height= size
			return np.zeros((height, width, 3),np.uint8)

		if isinstance(img, tuple):self.img = _makeimg((img[0],img[1]))     #new
		if isinstance(img, str):self.img = cv2.imread(img)                 #read
		if isinstance(img, np.ndarray):self.img = img.copy()               #reuse

	def raw(self):
	#画像そのまま返す
		return self.img

	def expand(self,scale):
	#scale倍(自然数)の画像にする
		y ,x ,_ = self.img.shape		
		copyimg = np.zeros((y*scale, x*scale, 3),np.uint8)
		for _x, _y in itertools.product(range(x), range(y)):
			B,G,R = self.img[_y,_x]
			color = (int(B),int(G),int(R))
			cv2.rectangle(copyimg,(_x*scale,_y*scale),(((_x+1)*scale),((_y+1)*scale)),color,-1)
		return copyimg

	def make_data(self):
	#画像からマップデータに変換

		def _replace(color):
		#色→数値への変換
			#           ( B , G , R )
			if color == (  0,  0,  0):return 0
			else:return 0

		y ,x ,_ = self.img.shape
		mapdata = np.empty((y,x),dtype=int)
		for _x, _y in itertools.product(range(x), range(y)):
			B,G,R = img[_y,_x]
			mapsec[_y,_x] = _replace((B,G,R))
		return mapdata

	def grid(self,row=1,col=1,color=(255,255,255)):
		#分割ラインを描画
		y ,x ,_ = self.img.shape
		row = [ (( 0, math.floor(y*i/row) ),( x, math.floor(y*i/row) )) for i in range(row)[1:] ]
		col = [ (( math.floor(x*i/col), 0 ),( math.floor(x*i/col), y )) for i in range(col)[1:] ]
		for i in row: cv2.line(self.img, *i , color)
		for i in col: cv2.line(self.img, *i , color)
		return self.img


class Visualize:#cv2表示補助
	def __init__(self,process_class):
		self.name =	" "
		self.base_img = None #背景画像
		self.step_img = None #変更した画像
		self.wait = 1

		self.display(process_class(self))

	def display(self,process_class):
		def reset(self):
			#意図的な例外の発生,exceptにつなぐ
			if self.window_getsize(self.name) == None:sys.exit()
			self.step_img = self.base_img.copy()

		def render(self):
			cv2.imshow(self.name,self.step_img)
			cv2.waitKey(self.wait)

		def close(self):
			cv2.destroyAllWindows()

		cv2.namedWindow(self.name)#表示窓作成
	#try:
		while(True):
			reset(self)
			process_class.main(self)
			render(self)
	#except:
		close(self)

	def window_getsize(self,window_name):
		#ｳｨﾝﾄﾞｳがないときNone
		#ｳｨﾝﾄﾞｳがあるとき表示ｻｲｽﾞ
		handle = win32gui.FindWindow(None,window_name)
		if handle == 0 : return None 
		rect = win32gui.GetWindowRect(handle)
		#ｽﾞﾚが出るので補正有
		width = rect[2]-rect[0]-16
		height= rect[3]-rect[1]-39
		return width,height

if __name__ == "__main__":
	pass

