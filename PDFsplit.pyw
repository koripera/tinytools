"""
PDFﾌｧｲﾙのﾍﾟｰｼﾞ分割を行う

分割したいPDFﾌｧｲﾙを引数で指定
"""

import PyPDF2

import os
import sys

def main():
	file1 = sys.argv[1]
	basepath = file1.rsplit('\\', 1)[0]
	 
	#PDFを読み込みオブジェクトを生成
	reader = PyPDF2.PdfFileReader(sys.argv[1])
	 
	#PDFのページ数を取得
	page_num = reader.getNumPages() 
	 
	#PDFを分割
	for page in range(page_num):
		writer = PyPDF2.PdfFileWriter() 
		p = reader.getPage(page)
		writer.addPage(p)
		
		#分割したPDFに名前を付けて保存
		fnum = '{0:03d}'.format(page+1)
		newpdf = os.path.join("./item/", f'美しく正しい字が書けるペン字練習帳_{fnum}.pdf')
		with open(newpdf, mode='wb') as f:
			writer.write(f)

if __name__ == "__main__":
	main()
