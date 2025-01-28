import sys

import cv2
import win32gui

class Frame:#cv2表示補助
	def __init__(self):
		self.name     =	" "
		self.base_img = None #基礎画像
		self.nomove_img = None #不動OBJ描画画像
		self.moving_img = None #動的OBJ描画画像
		self.wait     = 1

		self.scale   = 1

		self.moved_Default = (0,0)
		self.moved         = (0,0)

		self.mouse_L = False 

		self.changed = True #画面変更のキャッチ

		cv2.namedWindow(self.name)#表示窓作成
		cv2.setMouseCallback(self.name, self.mouseEvents)

	def reset(self):
		if self.window_getsize(self.name) == None:sys.exit()
		if self.changed:self.nomove_img = self.base_img.copy()
		self.moving_img = self.nomove_img.copy()

	def render(self):
		cv2.imshow(self.name,self.moving_img)
		cv2.waitKey(self.wait)		

	def close(self):
		cv2.destroyAllWindows()

	def mouseEvents(self,event, x, y, flags, param):
		try:
			if event == cv2.EVENT_LBUTTONDOWN:
				self.cricked = (x-self.moved[0],y-self.moved[1])
				self.mouse_L = True

			elif event == cv2.EVENT_LBUTTONUP:
				self.mouse_L = False

			elif event == cv2.EVENT_MBUTTONDOWN:
				self.scale=1
				self.moved = self.moved_Default
				self.changed = True				

			elif event == cv2.EVENT_MOUSEMOVE:
				if self.mouse_L:
					self.moved = (x-self.cricked[0] ,y-self.cricked[1])
					self.changed = True	
	
			elif event == cv2.EVENT_MOUSEWHEEL:
				if   flags>0:
					self.scale +=0.05
				elif flags<0:
					self.scale -=0.05
					if self.scale <= 0:self.scale +=0.05
				self.changed = True

		except Exception as e:
			print(e)


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

	@property
	def Default(self):
		return self.moved_Default

	@Default.setter
	def Default(self, posdata):
		self.moved_Default = posdata
		self.moved         = posdata
