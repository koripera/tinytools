"""
PDFﾌｧｲﾙの結合を行う

結合したいPDFﾌｧｲﾙを引数で指定
"marge().pdf"で出力する
"""

import PyPDF2

import os
import sys

def main():

	#引数がなければ終了
	if len(sys.argv) == 1 : sys.exit()

	#引数最初のものを保存のﾍﾞｰｽにする
	basepath = sys.argv[1].rsplit('\\', 1)[0]

	merger = PyPDF2.PdfFileMerger()

	for path in sys.argv[1:]:
		merger.append(path)

	#保存ファイル名重複するならナンバー増やす
	num = 1

	while os.path.exists(f"{basepath}/marge({num}).pdf"):
		num+=1

	#保存
	merger.write(f"{basepath}/marge({num}).pdf")
	merger.close()

if __name__ == "__main__":
	main()
