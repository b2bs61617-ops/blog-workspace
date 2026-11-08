#!/bin/sh
# VIVANT最終回 追加2記事のX投稿(@chomotirend)。1回目の5本が終わってから3分おき
cd "$(dirname "$0")"; PY="C:/Users/ti071/AppData/Local/Programs/Python/Python312/python.exe"; export PYTHONUTF8=1
until [ "$(grep -c tweet_url logs/vivantfinal_x_20261108.log)" -ge 5 ] || grep -q Traceback logs/vivantfinal_x_20261108.log; do sleep 15; done
sleep 180
post(){ "$PY" tools/x_auto_post_buffer.py --account trend --text "$1" --hashtags "$2" --post-id $3 --url "$4"; }
post "ハッピーエンド…と思った瞬間、神田明神のアレ🚨 あの赤いものが置かれる意味、覚えてる？置いたのは誰なのか、乃木に下される次の任務は…考察が止まらない🔥" "#VIVANT #VIVANTep24 #別班 #堺雅人" 13029 https://chomoand.com/vivant-24-beppan-manju/
sleep 180
post "エリシャ…まさかの最期😭 そして最後まで見つからなかったアレは、ベキが妻のために選んだ場所に眠ってた。開けるカギはまさかの…あの子だった⚡" "#VIVANT #VIVANTep24 #役所広司 #堺雅人" 13030 https://chomoand.com/vivant-24-elisha-data/
