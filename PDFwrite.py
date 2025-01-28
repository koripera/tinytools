from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from PyPDF2 import PdfWriter, PdfReader
from textwrap import dedent
import io


def draw(pw):
	pass



	




	

	


import PyPDF2
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

### 既存PDFの読み込み###
path = "test.pdf"
base_pdf = PyPDF2.PdfReader(path)
p = base_pdf.pages[0]

### PDFを生成###
io_object = io.BytesIO()    # BytesIOオブジェクトの生成
pw = canvas.Canvas(io_object)
pw.setPageSize((p.mediabox.right,p.mediabox.top))
pdfmetrics.registerFont(TTFont("MSゴシック", "C:/Windows/Fonts/msgothic.ttc"))
pw.setStrokeColorRGB(0.1, 0.1, 0.1)

### 文字を描画 ###
draw(pw)
pw.save()

### BytesIOの読み込み ###
io_object.seek(0)
new_pdf = PdfReader(io_object)

### 新規PDFと既存のPDFをマージ ###
output = PdfWriter()
p.merge_page(new_pdf.pages[0])
output.add_page(p)

### PDFを保存 ###
output_name = "output.pdf"
output_stream = open(output_name, 'wb')
output.write(output_stream)
output_stream.close()




