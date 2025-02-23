import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRect

import pytesseract
from PIL import Image,ImageEnhance,ImageFilter
import pyperclip
import json

def TextProcessor(text):
	"""テキストの処理を行う"""
	try:
		# 空白文字の削除
		text = ''.join(text.split())
		
		# 置換ルールを外部から読み込み
		with open('replacements.json', 'r', encoding='utf-8') as f:
			replacements = json.loads(f.read())

		print(replacements.items())	
		for old, new in replacements.items():
			text = text.replace(old, new)
		
		return text.strip()
		
	except Exception as e:
		logging.error(f"テキスト処理中にエラー: {e}")
		return text

def ocr(img):

	#ﾘｻｲｽﾞ
	img = img.resize((img.width * 3, img.height * 3), Image.LANCZOS)

	#ｸﾞﾚｰｽｹｰﾙ
	img = img.convert("L")

	#ﾉｲｽﾞ除去
	img = img.filter(ImageFilter.MedianFilter(size=3))

	#ｺﾝﾄﾗｽﾄ強調
	img = ImageEnhance.Contrast(img)
	img = img.enhance(2.0)

	#二値化
	threshold = 150  # 0〜255 の範囲で調整
	img = img.point(lambda x: 255 if x > threshold else 0)



	#img.show()
	text = pytesseract.image_to_string(img,lang="jpn")
	return text
	

def qpixmap_to_pil(pixmap):
	"""QPixmap → PIL Image"""
	qimage = pixmap.toImage()
	buffer = qimage.bits().asstring(qimage.byteCount())
	img = Image.frombytes("RGBA", (qimage.width(), qimage.height()), buffer)
	return img.convert("RGB")  # RGBA → RGB

class ScreenCapture(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("スクリーンショット選択")
		self.setGeometry(100, 100, 800, 600)
		self.setWindowOpacity(0.3)  # ウィンドウの透過
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 枠なし＆最前面
		self.start_pos = None  # ドラッグ開始位置
		self.end_pos = None  # ドラッグ終了位置
		self.drawing = False  # 描画中フラグ
		self.showFullScreen()  # 全画面表示

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.start_pos = event.globalPos()
			self.drawing = True

	def mouseMoveEvent(self, event):
		if self.drawing:
			self.end_pos = event.globalPos()
			self.update()  # 描画更新

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.drawing = False
			self.captureScreen()
			self.close()

	def paintEvent(self, event):
		if self.start_pos and self.end_pos:
			qp = QPainter(self)
			qp.setRenderHint(QPainter.Antialiasing)

			# **1. 画面全体を暗くする**
			qp.setBrush(QColor(0, 0, 0, 150))  # 黒 (透過度150)
			qp.drawRect(self.rect())

			# **2. 選択範囲をクリア**
			selection_rect = QRect(self.start_pos, self.end_pos).normalized()
			qp.setCompositionMode(QPainter.CompositionMode_Clear)  # クリアモード
			qp.fillRect(selection_rect, Qt.transparent)

			# **3. 選択範囲の枠を描画 (キャプチャには含めない)**
			qp.setCompositionMode(QPainter.CompositionMode_SourceOver)  # 通常描画モードに戻す
			qp.setPen(QColor(255, 0, 0, 150))  # 赤い枠 (透明度150)
			qp.drawRect(selection_rect)

	def captureScreen(self):
		if self.start_pos and self.end_pos:
			rect = QRect(self.start_pos, self.end_pos).normalized()
			screen = QApplication.primaryScreen()
			
			# **スクショ取得時には枠を含めない**
			screenshot = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())

			#PIL形式に変換
			pic = qpixmap_to_pil(screenshot)

			#tesseractに渡す
			text = ocr(pic)

			text = TextProcessor(text)

			#クリップボードに
			pyperclip.copy(text)
			print(repr(text))
			#screenshot.save("screenshot.png", "PNG")
			#print("スクリーンショットを保存しました: screenshot.png")

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:  # ESCキーでキャンセル
			self.close()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = ScreenCapture()
	sys.exit(app.exec_())

