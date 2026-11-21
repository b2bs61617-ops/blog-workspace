cd /c/Users/s30se/Desktop/blog-workspace
export XIY_NO_REPLIES=1
d=tools/Xiy/mag_acc_2026_extra
run(){ python tools/Xiy/x_collector.py --keyword "$2" --no-ai --out $d/$1 > $d/$1.log 2>&1; }
run sm_itadaki '(SnowMan OR "Snow Man") (着用頂き OR 着用頂い OR 雑誌掲載情報 OR 着用情報) since:2026-01-01'
run st_itadaki '(SixTONES OR ストーンズ) (着用頂き OR 着用頂い OR 雑誌掲載情報 OR 着用情報) since:2026-01-01'
run tj_itadaki '("Travis Japan" OR TravisJapan OR トラジャ) (着用頂き OR 着用頂い OR 雑誌掲載情報 OR 着用情報) since:2026-01-01'
