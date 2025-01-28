"""
ﾌｧｲﾙの分類を行う

指定ﾌｫﾙﾀﾞ内の、()が付いたﾌｧｲﾙを、
()を除いた名前のﾌｫﾙﾀﾞに移動させる
"""

import os
import shutil

#--------------
#対象のﾌｫﾙﾀﾞﾊﾟｽを記入すること

path = "testtest"

#--------------

def main():
	#ﾌｫﾙﾀﾞﾊﾟｽ内の内容物を取得
	contents = os.listdir(path)

	#ﾌｧｲﾙのみを抽出
	files = [content for content in contents 
			if os.path.isfile(os.path.join(path, content))
			]

	#()が付いてるﾌｧｲﾙを対象にする
	target_files = [filename for filename in files if "(" in filename]

	#ﾌｧｲﾙ毎に繰り返し
	for filename in target_files:

		#右端の括弧から右を除外し、ﾌｫﾙﾀﾞ名を作る
		index = filename.rfind("(")
		dirname = filename[:index]

		#ﾌｫﾙﾀﾞがなければ新規作成
		if not os.path.exists(os.path.join(path, dirname)):
			os.makedirs(os.path.join(path, dirname))

		#ﾌｧｲﾙの移動
		shutil.move(os.path.join(path, filename),os.path.join(path, dirname))
	
if __name__ == "__main__":
	main()
