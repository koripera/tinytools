import cv2
import numpy as np
import sys
import math
import random
import win32gui 

#--------------------
window_name = "frame"
window_size = (500,500)


#--------------------

def main():
	p=Point()
	setup(window_name,window_size)
	cv2.setMouseCallback(window_name, onMouse,p)
	
	while(True):
		if getsize(window_name) == None:
			sys.exit()

		#背景・画像の作成
		frame = makeimage(getsize(window_name))
		img = mainimage()

		#背景・画像の合成
		frame = combine_image(frame,img,(p.x,p.y))

		cv2.imshow(window_name,frame)

		k = cv2.waitKey(1)
		if k == ord("q"):
			break
		if k == ord("r"):
			p.x,p.y=0,0

	cv2.destroyAllWindows()

def combine_image(base_img,top_img,point):
	#画像合成を行う関数
	#base_img:背景画像  top_img:追加画像  point:追加画像の左上座標

	#画像がはみ出る場合...はみ出る部分を画像にしないようにする
	#追加画像のｶｯﾄしたｻｲｽﾞと、背景画像の置換範囲は一緒の必要がある

	#sx,sy,ex,eyはstart-end,x-yの略
	#画像を全て選択 ---→ img[0:img_h, 0:img_w]
	#画像を範囲選択 ---→ top_img[ top_sy : top_ey , top_sx : top_ex ]
	#基本の置換範囲---→  base_img[ y : y+top_h , x : x+top_w ]

	x,y = point
	base_h, base_w = base_img.shape[:2]
	top_h, top_w = top_img.shape[:2]
	
	top_sx,top_sy=0,0
	top_ex,top_ey= top_w,top_h

	replace_sx,replace_sy = x , y
	replace_ex,replace_ey = (x+top_w) , (y+top_h)

	#画面外にでる場合
	#左端外,上端外,右端外,下端外
	if (x+top_w)<0 or (y+top_h)<0 or base_w<x or base_h<y:
		return base_img

	#左端が出る
	if x < 0:
		#描画範囲→ はみ出しxから通常xまで
		top_sx = top_sx + abs(x) 

		#置換範囲→ (左端 から(top画幅-はみ出し))
		replace_sx = 0           
		replace_ex = top_w - abs(x)

	#上端が出る
	if y < 0:
		#描画範囲→ はみ出しyから通常yまで
		top_sy = top_sy + abs(y) 

		#置換範囲→ (上端 から(top画高-はみ出し))
		replace_sy = 0           
		replace_ey = top_h - abs(y)

	#右端が出る
	if base_w < (x + top_w):
		#描画範囲→ 通常xからはみだしxまで
		outrange = (x + top_w) - base_w
		top_ex = top_w - outrange

		#置換範囲→ (通常x から右端)          
		replace_ex = base_w

	#下端が出る
	if base_h < (y + top_h):
		#描画範囲→ 通常yからはみだしyまで
		outrange = (y + top_h) - base_h
		top_ey = top_h - outrange

		#置換範囲→ (通常y から下端)          
		replace_ey = base_h
	
	base_img[ replace_sy:replace_ey, replace_sx:replace_ex ]= \
	top_img[ top_sy : top_ey , top_sx : top_ex ]
	return base_img

def setup(window_name,window_size):#windowなど表示準備
	w,h=window_size
	cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
	cv2.resizeWindow(window_name, w, h)

def makeimage(size):#指定sizeのnp配列を返す
	width,height= size
	image = np.zeros((height, width, 3),np.uint8)

	txt(image, '    q:quit',10)
	txt(image, 'other:move',20)

	return image.copy()

def getsize(window_name):	
	handle = win32gui.FindWindow(None,window_name)
	if handle == 0:
		return None
	rect = win32gui.GetWindowRect(handle)
	width = rect[2]-rect[0]-16
	height= rect[3]-rect[1]-39
	return width,height
		
def mainimage():
	img = np.zeros((100, 200, 3))
	img += 255
	return img.copy()


def onMouse(event, x, y, flags, params):
	p = params

	if event == cv2.EVENT_LBUTTONDOWN:
		p.L_click = True
		p.click_x,p.click_y= x,y#ｸﾘｯｸ位置を保存
		p.old_x,p.old_y= p.x,p.y#変更前位置を保存
		
	if event == cv2.EVENT_LBUTTONUP:		
		p.L_click = False
		p.click_x,p.click_y= None,None#ｸﾘｯｸ位置を削除
		print(p.x,p.y)

	if event == cv2.EVENT_MOUSEMOVE and p.L_click:#ﾄﾞﾗｯｸﾞ時動作
		p.x = p.old_x+(x-p.click_x)#画像の移動(変更前座標+移動量)
		p.y = p.old_y+(y-p.click_y)

class Point:
	def __init__(self):
		self.x=0 #今の位置
		self.y=0
		self.L_click = None
		self.click_x =None
		self.click_y =None
		self.old_x = None
		self.old_y =None

def maindraw(frame,data):
	auto = 0 #0:コマ送り 1:自動送り
	return auto

def txt(frame,moji,posi):
	t_position  = (0, posi)
	t_font      = cv2.FONT_HERSHEY_SIMPLEX
	t_fontscale = 0.4
	t_color     = (255, 255, 255)
	cv2.putText(frame,moji,t_position,t_font, t_fontscale, t_color, 1, cv2.LINE_8)
	
def pixel(canvas,x,y,color):#1pixelの変更
		canvas.itemset((y, x, 0), color[0])
		canvas.itemset((y, x, 1), color[1])
		canvas.itemset((y, x, 2), color[2])

class drow:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.angle = 0

	def v(self,frame,point,length,angle):
		aplus = 10
		self.x,self.y = point
		self.angle = angle
		lx,ly = drow().line_long(frame,point,length,angle+aplus)
		rx,ry = drow().line_long(frame,point,length,angle-aplus)
		la =angle+aplus
		ra =angle-aplus
		return {"lx":lx,"ly":ly,"la":la,"rx":rx,"ry":ry,"ra":ra}

	def line_long(self,frame,point,length,angle):
		self.x,self.y = point
		self.angle = angle
		movex = round(math.cos(math.radians(self.angle))*length) +self.x
		movey = round(math.sin(math.radians(self.angle))*length) +self.y

		cv2.line(frame, (self.x, self.y), (movex, movey), (255, 255, 255))
		return movex, movey
		
if __name__ == "__main__":
	main() 
