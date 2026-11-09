# -*- coding: utf-8 -*-
"""15556: NARUTO節を「DAIKIもNARUTO好きなのかも？」のニュアンスに(本人発言は未確認のため断定しない)。オシリ指示 2026-11-10"""
import sys, json, requests
sys.path.insert(0, '.')
from _mubank1009_helpers import WP_URL, HEADERS_AUTH
PID = 15556
raw = requests.get(f'{WP_URL}/wp-json/wp/v2/posts/{PID}', params={'context': 'edit'}, headers=HEADERS_AUTH).json()['content']['raw']
OLD_H = 'KO1KEYZにはNARUTO好きが多い？'
NEW_H = 'DAIKIもNARUTO好きなのかも？'
OLD_P = '''そこに今回、DAIKIが我愛羅のひょうたんバッグで登場したことで、グループの中にNARUTO好きが2人いることになりました。<br>
これからDAIKIとRYOGAの2人で、NARUTOの話で盛り上がる場面も見られるかもしれませんね。'''
NEW_P = '''そこに今回、DAIKIが我愛羅のひょうたんバッグで登場しました。<br>
DAIKI本人が「NARUTOが好き」と話した場面はまだ確認できていませんが、高さ60cm以上もある我愛羅のひょうたんを空港に持ってくるくらいなので、DAIKIもNARUTO好きなのかもしれません。<br>
もしそうなら、KO1KEYZにはNARUTO好きが2人いることになりますね。<br>
これからDAIKIとRYOGAの2人で、NARUTOの話で盛り上がる場面も見られるかもしれません。'''
assert raw.count(OLD_H) == 1 and raw.count(OLD_P) == 1
raw = raw.replace(OLD_H, NEW_H).replace(OLD_P, NEW_P)
r = requests.post(f'{WP_URL}/wp-json/wp/v2/posts/{PID}', headers={**HEADERS_AUTH, 'Content-Type': 'application/json'},
                  data=json.dumps({'content': raw}).encode('utf-8'))
r.raise_for_status(); print('updated', PID, r.json()['status'])
