import requests
from pathlib import Path
import tqdm

if True:
	#作成するフレーズのテキスト
	with open("phrase.txt", encoding="utf-8") as f:
		s = f.read()

	sl = s.split("\n")

	save_dir = sl[0]
	wordlist = [e for e in sl[1:] if e!="" and e[0]!="#"]

	url = "http://localhost:50021/audio_query"

	for word in tqdm.tqdm(wordlist):
		params = {"text": word, "speaker": 3}  # ずんだもん ノーマルスタイル
		timeout = 15
		query_synthesis = requests.post(url, params=params, timeout=timeout)

		# params = {"speaker": 3}
		response = requests.post(
					"http://localhost:50021/synthesis",
					params=params,
					json=query_synthesis.json(),
				)
		wav = response.content

		path = f"{save_dir}/{word}.wav"  # 保存場所
		out = Path(path)
		out.write_bytes(wav)

if False:
	#(参考)
	#https://qiita.com/kaguraluna/items/5c1fbe124bbdd0f33bac

	import requests
	from pathlib import Path

	url = "http://localhost:50021/audio_query"
	params = {"text": "これはサンプルボイスです", "speaker": 3}  # ずんだもん ノーマルスタイル
	timeout = 15
	query_synthesis = requests.post(url, params=params, timeout=timeout)

	# params = {"speaker": 3}
	response = requests.post(
				"http://localhost:50021/synthesis",
				params=params,
				json=query_synthesis.json(),
			)
	wav = response.content

	path = "sample.wav"  # 保存場所
	out = Path(path)
	out.write_bytes(wav)
