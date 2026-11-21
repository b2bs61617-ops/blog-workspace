cd /c/Users/s30se/Desktop/blog-workspace
export XIY_NO_REPLIES=1
q1='(SnowMan OR "Snow Man" OR スノーマン) 着用いただき since:2026-01-01'
q2='(SnowMan OR "Snow Man") 着用 (リング OR ネックレス OR ピアス OR イヤーカフ OR ブレスレット OR バングル) since:2026-01-01'
q3='(岩本照 OR 深澤辰哉 OR ラウール OR 渡辺翔太 OR 向井康二 OR 阿部亮平 OR 目黒蓮 OR 宮舘涼太 OR 佐久間大介) 着用いただ since:2026-01-01'
i=1
for q in "$q1" "$q2" "$q3"; do
  python tools/Xiy/x_collector.py --keyword "$q" --no-ai --out tools/Xiy/sm_mag_acc_2026/q$i > tools/Xiy/sm_mag_acc_2026/q$i.log 2>&1
  i=$((i+1))
done
