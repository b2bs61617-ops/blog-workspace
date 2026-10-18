#!/bin/sh
# VIVANT21話 5記事のX投稿(@chomotirend)。Buffer接続後にこれを実行すれば即時投稿される。
cd "$(dirname "$0")"; PY="C:/Users/ti071/AppData/Local/Programs/Python/Python312/python.exe"; export PYTHONUTF8=1
post(){ "$PY" tools/x_auto_post_buffer.py --account trend --text "$1" --hashtags "$2" --post-id $3 --url "$4"; }
post "VIVANT21話、リュウが「ご褒美」に野崎を求めた理由は？ドラムを麻酔銃で眠らせて2人きりに…キスに見えた場面の真相と、リュウは裏切り者か味方かを考察しました。" "#VIVANT #VIVANTep21 #堺雅人 #阿部寛" 12590 https://chomoand.com/vivant-21-ryu-nozaki-reward/
post "VIVANT21話、ノコルの「お前、誰だ？」にF「さすがに気づいたか」。ノコルがFに気づいた理由と、「F」「兄さん」の呼び分けから見える人格統合説を考察しました。" "#VIVANT #VIVANTep21 #二宮和也 #堺雅人" 12592 https://chomoand.com/vivant-21-nokoru-omae-dareda/
post "VIVANT21話、脱出を手引きしたナティックは裏切り者？検問で前にいた車のおばあさん、やらかし続きの東条は？21話で怪しまれた人物をまとめて考察しました。" "#VIVANT #VIVANTep21 #堺雅人 #二宮和也" 12594 https://chomoand.com/vivant-21-natick-traitor/
post "VIVANT21話、リュウに撃たれたドラムは無事？撃たれたのは麻酔銃だったとみられます。眠らせた理由と「10人前」の伏線、ドラムの今後を考察しました。" "#VIVANT #VIVANTep21 #富栄ドラム #堺雅人" 12596 https://chomoand.com/vivant-21-drum-alive/
post "VIVANT21話、Fの「やつがここにいないのはおかしい」は周のこと？ラストで検問に現れた周はなぜ先回りできたのか。22話の展開を予想しました。" "#VIVANT #VIVANTep21 #堺雅人 #日曜劇場" 12598 https://chomoand.com/vivant-21-amane-yatsu/
