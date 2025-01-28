from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

import re
import os
from decimal import Decimal, ROUND_HALF_UP

import unicodedata

import PyPDF2

output_file = ".pdf"

def main():
	data1 =".pdf"
	data2 =".pdf"

	data1 = PyPDF2.PdfReader(data1)
	data2 = PyPDF2.PdfReader(data2)
	writer = PyPDF2.PdfWriter()

	# 繋ぎ合わせるページ（p1：左側、p2：右側）
	p1 = data1.pages[0]
	p2 = data2.pages[0]

	# 見開きにしたページサイズ
	total_width = p1.mediabox.right + p2.mediabox.right
	total_height = max([p1.mediabox.top, 
						p1.mediabox.top])

	# ページを貼り付ける空白ページ
	p = PyPDF2.PageObject.create_blank_page(width=total_width, 
											  height=total_height)

	# 見開きにするため、右ページ用のPDFを右に平行移動、mediaboxもそれに合わせて右に平行移動
	op = PyPDF2.Transformation().translate(tx=p1.mediabox.right)
	p2.add_transformation(op)
	p2.mediabox.left = p1.mediabox.right
	p2.mediabox.right = p1.mediabox.right + p2.mediabox.right

	p.merge_page(p1)
	p.merge_page(p2)
	writer.add_page(p)

	with open(output_file, mode="wb") as f:
		writer.write(f)



if __name__ == "__main__":
	main() 
