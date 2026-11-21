cd /c/Users/s30se/Desktop/blog-workspace
export XIY_NO_REPLIES=1
d=tools/Xiy/st_tj_mag_acc_2026
run(){ python tools/Xiy/x_collector.py --keyword "$2" --no-ai --out $d/$1 > $d/$1.log 2>&1; }
run st1 '(SixTONES OR ストーンズ) 着用いただき since:2026-01-01'
run st2 '(ジェシー OR 京本大我 OR 松村北斗 OR 髙地優吾 OR 高地優吾 OR 森本慎太郎 OR 田中樹) 着用いただ since:2026-01-01'
run tj1 '("Travis Japan" OR トラジャ OR TravisJapan) 着用いただき since:2026-01-01'
run tj2 '(宮近海斗 OR 中村海人 OR 七五三掛龍也 OR 川島如恵留 OR 吉澤閑也 OR 松田元太 OR 松倉海斗) 着用いただ since:2026-01-01'
