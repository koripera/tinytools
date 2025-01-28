from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

import re
import os
from decimal import Decimal, ROUND_HALF_UP

import unicodedata

#------------------------------
#テキストファイルを読み込み、縦A5用紙に2コラムのPDFを出力します

#読み込むテキストファイル
input_text = ".txt"

#出力するPDFファイル
output_pdf = ".pdf"

#------------------------------

def main():
	page = pdfdata(output_pdf,148,210)

	f = open(input_text,"r",encoding="utf-8") 
	rawtxt = f.read()
	f.close()
	txtdata = rawtxt.split("\n")

	page.notebook(txtdata)

	page.save()


def get_east_asian_width_count(text):
	count = 0
	for c in text:
		if unicodedata.east_asian_width(c) in 'FWA':
			count += 2
		else:
			count += 1
	return count

def strcut(txt,wantlong):#文字列先頭から欲しい長さを求める
	num = 0
	maxnum = len(txt)
	localtxt = txt
	txtlist = []

	while True:
		count = get_east_asian_width_count(localtxt[0:num])#文字数のカウント
		if count > wantlong:#欲しい長さを超えた時
			txtlist.append( localtxt[0:num-1] )#頭の文字を抜き取る
			localtxt = localtxt[num-1:]
			num = 0
			continue

		num = num+1

		if num > maxnum:
			txtlist.append( localtxt[:num-1] )
			break
	
	return txtlist




















class pdfdata:
#pdfdata()  (str/名前 int/横ｻｲｽﾞ int/縦ｻｲｽﾞ int/ﾌｫﾝﾄｻｲｽﾞ str/ﾌｫﾝﾄ名 dic/余白)
	setup = False

	def setting(self):
		pdfmetrics.registerFont(TTFont("MSゴシック", "C:/Windows/Fonts/msgothic.ttc"))

	def __init__( self , name , width , height , fontsize=6 , font="MSゴシック",margin = {"top":5, "bottom":5, "right":5, "left":5}):
		if pdfdata.setup == False:
			self.setting()
			pdfdata.setup = True
			
		self.x,self.y = 0,0  #原点
		self.name = name
		self.width = width
		self.height = height
		self.fontsize = fontsize
		self.font = font
		self.margin = margin
 
		#self.file_path =os.path.expanduser("~") + "/Desktop/" + self.name
		self.file_path = self.name
		self.page = canvas.Canvas(self.file_path)
		#フォントサイズ(mm)を計算
		self.fontsize_mm = float(Decimal(str( fontsize * 0.35278 )).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

		self.page.setPageSize((self.width*mm, self.height*mm))
		# フォントの設定(第1引数：フォント、第2引数：サイズ)
		self.page.setFont(font, fontsize)
		#線を細くして見やすく
		self.page.setStrokeColorRGB(0.1, 0.1, 0.1)  #どっちかあることで空白のページになる、他に記述ないとPDF開けない
		self.page.setLineWidth(0.05)                #→↑ 

	def newpage(self):
		self.page.showPage()
		self.page.setFont(self.font, self.fontsize)

	def notebook(self,txtdata):

		#改行の調整
		newlist=[]
		for i in txtdata:
			count = get_east_asian_width_count(i)

			if count <= 64:
				newlist.append(i)
			
			if count > 64:
				for n in strcut(i,64):
					newlist.append(n)

		txtdata = newlist


		#レイアウト
		x_center = self.width/2
		chara_half = self.fontsize_mm/2
		x_center_hidari = x_center - chara_half
		x_center_migi = x_center + chara_half
		writearea_yoko = self.width - self.margin["left"] - self.margin["right"]
		lines = int((self.height - self.margin["top"] - self.margin["bottom"])/self.fontsize_mm)

		#左のコラム分
		write_line = 0
		pattern = "【.*?】"
		while write_line < len( txtdata ):

			rows = 1
			for i in txtdata[ write_line :]:#0~94 188~
				if re.fullmatch(pattern, i) and rows != 1:break #ﾒｲﾝﾀｲﾄﾙが来たら、別ページに
				if write_line == len( txtdata ) : break         #書ききったら終わり
				if rows > lines:break                           #最終行書いたら次に
				x = self.margin["left"]
				y = self.height - self.margin["top"] - rows * self.fontsize_mm
				self.page.drawString(x*mm, y*mm, i)
				write_line +=1 
				rows = rows + 1

			#右のコラム分
			rows = 1
			for i in txtdata[ write_line:]:#94~188
				if re.fullmatch(pattern, i):break
				if write_line == len( txtdata ) : break
				if rows > lines:
					self.newpage()
					break
				x = x_center_migi
				y = self.height - self.margin["top"] - rows * self.fontsize_mm
				self.page.drawString(x*mm, y*mm, i)
				write_line +=1
				rows = rows + 1

			if write_line < len( txtdata ):
				if re.fullmatch(pattern, txtdata[ write_line ]):
					self.newpage()




	def save(self):
		self.page.save()








if __name__ == "__main__":
	main() 
