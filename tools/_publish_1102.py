# 2026-11-02 Snow Man 7本 + トラジャ下書き7本を公開→Indexing→X/Threadsを3分おきに即時投稿
import os, sys, time, subprocess, requests
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for l in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip("\"'"))
def site(n):
    return os.environ[f"WP_CHOMO{n}_URL"].rstrip("/"), (os.environ[f"WP_CHOMO{n}_USERNAME"], os.environ[f"WP_CHOMO{n}_APP_PASSWORD"])
PY = sys.executable
POSTS = [
    (2, 398, "Snow Manでいちばん早く入所したの誰か言える？😳✨\n同じ日に入った2人がいて、最年少入所はまさかの10歳…！末っ子とは10年以上差があるの尊すぎて泣く😭💕", "#SnowMan #すの担"),
    (2, 408, "ラウールくん、1人で王様6役ってなに😭👑💕\nコンサートで振れそうな特大うちわがもらえるの、すの担的に優勝案件すぎる…！もらえる条件ちゃんと調べたよ🫶", "#SnowMan #ラウール"),
    (2, 431, "照くんの空港コーデ、全身黒で強すぎて無理😭🖤\n肩にかけてた大きいレザーバッグ、お値段50万超え…！幅48cmってどんなサイズ感なの👀", "#SnowMan #岩本照"),
    (2, 416, "さっくんのスイス旅行の空港ショット、ピンク髪×白トラックトップ可愛すぎて無理😭💗\nトップスだけで40万超え…スーツケースの上のバッグはまさかのスエード👀✨", "#SnowMan #佐久間大介"),
    (2, 421, "照くんがミラノで着てたふわふわ水色カーディガン、破壊力えぐい😭🩵\n水玉シャツと合わせたらお値段80万超え…！耳もとでゆれるピアスも見逃せない👀", "#SnowMan #岩本照"),
    (2, 426, "めめの胸元の扇形ネックレス、色とりどりの石がキラッキラすぎた😭💎\n168日ぶりの「ただいま」で着けてたジュエリー全5点、時計まで入れると桁がおかしい…🫠", "#SnowMan #目黒蓮"),
    (2, 436, "照くんがトーストかじってた温室みたいなカフェ、おしゃれすぎて行きたい😭☕️\n黄色いリゾットのお店も街角の交差点も、写真の場所ぜんぶ調べたよ🇮🇹✨", "#SnowMan #岩本照"),
    (4, 2019, "トラジャでいちばん早く入所したのは誰？😳\nトリプルカイトが同じ日入所なの尊すぎない…？最年少入所は11歳、入所のきっかけも泣ける😭💕", "#TravisJapan #トラジャ"),
    (4, 2028, "今週のトラジャ、7人そろう番組もあるし金ローにはげんげんの声が…！😭🦁\n深夜に放送再開する番組もあるから録画予約はお早めに📺✨", "#TravisJapan #トラジャ"),
    (4, 2032, "しめちゃんのハロウィンカチューシャ可愛すぎて無理😭🎃\nフライパンひとつ・15分で作れるチーズとろ〜りの一品、TJの飾りつけまで真似したい🧀✨", "#TravisJapan #七五三掛龍也 #七五三掛KITCHEN"),
    (4, 2055, "4周年生配信のげんげん、キラキラシャツの袖からのぞく金色の時計に釘付け😭✨\n水色の文字盤が爆イケすぎ…お値段も震えるレベルだった🫠", "#TravisJapan #松田元太"),
    (4, 2081, "はだかんぼうたち5話、鯖崎の「好きな人だよ」で情緒ぶっ壊れた😭💕\n雨上がりにふたりが歩いた場所もワインを選んだお店も実在してた…聖地巡礼したすぎる👀✨", "#TravisJapan #松田元太 #はだかんぼうたち"),
    (4, 2109, "5話の鯖崎、衣装がいちばん多い回だったの気づいた？😭🖤\n表参道デートの黒ワントーンも夜のダブルスーツも色気えぐすぎ…新しく入った衣装協力ブランドも調べたよ👔✨", "#TravisJapan #松田元太 #はだかんぼうたち"),
    (4, 2115, "トラジャ2027ツアー、いちばん激戦の公演どこだと思う？😱🔥\n1,283人分の申込状況を集計したら、数字のうえでねらい目の会場も見えてきた…！🎫", "#TravisJapan #トラジャ #JewelryBasket"),
]
links = {}
for n, pid, _, _ in POSTS:
    U, A = site(n)
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", json={"status": "publish"}, auth=A, timeout=60).json()
    links[pid] = r.get("link"); print("PUBLISH", pid, r.get("status"), r.get("link"), flush=True)
    subprocess.run([PY, os.path.join(ROOT, "tools", "google_indexing.py"), r.get("link")], cwd=ROOT)
for i, (n, pid, text, tags) in enumerate(POSTS):
    if i: time.sleep(180)
    print("X", pid, time.strftime("%H:%M:%S"), flush=True)
    subprocess.run([PY, os.path.join(ROOT, "tools", "x_auto_post_buffer.py"), "--text", text, "--hashtags", tags,
                    "--post-id", str(pid), "--url", links[pid]], cwd=ROOT)
print("DONE", flush=True)
