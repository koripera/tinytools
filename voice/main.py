from flask import Flask, Response, request,render_template

from pydub import AudioSegment
from pydub.generators import Sine
import io
import socket
import ipget

import random
import glob

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('main.html')  # HTMLを返す

@app.route('/stream-audio')
def stream_audio():
	def generate_audio():

		max_repeats = 5  # 繰り返しの最大回数
		repeat_count = 0
		l1 = glob.glob('expand/**/*wav',recursive=True)
		l2 = glob.glob('word/**/*.wav',recursive=True)
		l3 = glob.glob('connect/**/*.wav',recursive=True)
		#print(*l1,*l2,sep="\n")

		while True:
			n = random.randrange(5)

			#補足+単語
			if n!=0:
				path1 = random.choice(l1)
				path2 = random.choice(l2)
				audio1 = AudioSegment.from_file(path1, format="mp3")
				audio2 = AudioSegment.from_file(path2, format="mp3")

				#連結
				combined = audio1[:-180] + audio2 + AudioSegment.silent(duration=2000)

			#単語+の+単語
			else:
				path1 = random.choice(l2)
				path0 = random.choice(l3)
				path2 = random.choice(l2)

				audio1 = AudioSegment.from_file(path1, format="mp3")
				audio0 = AudioSegment.from_file(path0, format="mp3")
				audio2 = AudioSegment.from_file(path2, format="mp3")

				audio0 = (audio0[:-150]+5).fade_in(200).fade_out(100)

				ms = 100#"単語+の"の重ね合わせの時間
				
				position = max(0,len(audio1) - ms)#
				#連結
				combined = audio1[:-210] + audio0 + audio2 + AudioSegment.silent(duration=2000)

				

			buffer = io.BytesIO()
			combined.export(buffer, format="mp3")
			buffer.seek(0)
			audio_data = buffer.read()
			
			if repeat_count >= max_repeats:
				repeat_count = 0  # カウントリセット
				buffer.seek(0)	# バッファをリセット
			yield audio_data
			repeat_count += 1

	return Response(generate_audio(), content_type="audio/mpeg")




if __name__ == '__main__':
	#ipの取得
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("192.168.100.1", 80))
		ip = s.getsockname()[0]
		s.close()
	except:
		ip = None

	print(ip)

	app.run(host=ip ,port=5000 ,debug=True)












if False:
	@app.route('/generate-audio')
	def agenerate_audio():
		# クエリパラメータから周波数と長さを取得（デフォルトは440Hz, 3秒）
		#frequency = int(request.args.get('freq', 440))  # 周波数 (Hz)
		#duration = int(request.args.get('duration', 3))  # 長さ (秒)

		# サイン波を生成
		#sine_wave = Sine(frequency).to_audio_segment(duration=duration * 1000)

		# メモリ上に書き込む
		buffer = io.BytesIO()
		audio.export(buffer, format="wav")
		buffer.seek(0)

		# レスポンスとしてWAVを返す
		return Response(buffer, mimetype="audio/wav")

	@app.route('/stream-audio')
	def stream_audio():
		def generate_audio():
			while True:  # 無限ループでデータを生成
				# メモリ上に音声データを書き出し
				buffer = io.BytesIO()
				audio2.export(buffer, format="mp3")
				buffer.seek(0)
				yield buffer.read()  # データをストリームとして送信
		
		return Response(generate_audio(), content_type="audio/mpeg")

	#音声の繰り返し
	@app.route('/stream-audio')
	def stream_audio():
		def generate_audio():
			buffer = io.BytesIO()
			audio2.export(buffer, format="mp3")
			buffer.seek(0)
			audio_data = buffer.read()
			
			max_repeats = 5  # 繰り返しの最大回数
			repeat_count = 0

			while True:
				if repeat_count >= max_repeats:
					repeat_count = 0  # カウントリセット
					buffer.seek(0)	# バッファをリセット
				yield audio_data
				repeat_count += 1

		return Response(generate_audio(), content_type="audio/mpeg")



