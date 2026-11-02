# 2026-11-02 SixTONES(chomoand-0.com)下書き8本を公開→Indexing→X/Threadsを3分おきに即時投稿
# ユカのMacはローカル.envのWP_AUDITION_*が空欄なので、SIXTONES_ENV_FILE(Googleドライブの.env)から読む
import os, sys, time, subprocess, requests
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(path):
    for l in open(path, encoding="utf-8"):
        l = l.strip()
        if l and not l.startswith("#") and "=" in l:
            k, v = l.split("=", 1)
            if v.strip().strip("\"'") and not os.environ.get(k.strip()):
                os.environ[k.strip()] = v.strip().strip("\"'")
load(os.path.join(ROOT, ".env"))
if os.environ.get("SIXTONES_ENV_FILE"):
    load(os.environ["SIXTONES_ENV_FILE"])
U = os.environ["WP_AUDITION_URL"].rstrip("/")
A = (os.environ["WP_AUDITION_USERNAME"], os.environ["WP_AUDITION_APP_PASSWORD"])
PY = sys.executable
POSTS = [
    (1235, "こーちが持ってる資格、THEバトルSHOWで知って沼確定した🫠♨️\nお風呂の入り方まで指導できるってなに…取ったのは7年前、きっかけが可愛すぎる😭💛", "#SixTONES #髙地優吾"),
    (1232, "11/4発売のMILESixTONES、フラゲ組の感想が供給過多すぎる🫠💿\nMCだけで170分超え…！初回盤と通常盤どっちにするか迷ってる人多すぎて違いまとめたよ🫶", "#SixTONES #MILESixTONES"),
    (1226, "SixTONESって公式のファンネーム、あると思う？👀\nスト担はみんな使うけど、樹くん発祥のもうひとつの呼び名も知ってた…？由来が反則すぎる😭", "#SixTONES #スト担 #田中樹"),
    (1229, "は？？マキタのCMにSixTONES…！？🔧😳\nチェンソー持った作業服ビジュ、職人みが強すぎて情緒ぶっ壊れた😭 出てるのは6人中3人、選ばれた理由が納得すぎる🔥", "#SixTONES #スト担"),
    (1223, "2026年のSixTONESリーダー、決め方がまさかのアレ…😳✊\n約32万人が見守る中で決まったのストらしすぎて優勝🏆 しかも本人はこれが初リーダーなんだって😭💕", "#SixTONES #スト担"),
    (1241, "スタジアムグッズの通販、まだ届いてない人いる？📦🥺\n2回目の受付が始まるタイミング、まさかの日産公演の真っ最中…！見逃し厳禁すぎる🚨", "#SixTONES #MILESixTONES"),
    (1244, "モデルプレス今年の顔、スト担の投票ラッシュ熱すぎる🔥🗳️\nじつは投票数だけじゃ決まらないって知ってた？締切まで毎日投票できるから今日の分まだの人は急いで😭", "#SixTONES #モデルプレス今年の顔"),
    (1238, "日産スタジアムのスト、開演時間が3会場でいちばん早いの気づいてた？😱⏰\n11月下旬の横浜の夜は想像以上に冷えるらしい…服装もう決めた？🧥✨", "#SixTONES #MILESixTONES"),
]
if __name__ == "__main__" and "--check" in sys.argv:
    w = lambda s: sum(1 if ord(c) < 128 else 2 for c in s)
    for pid, t, h in POSTS: print(pid, w(t + "\n" + h))
    sys.exit()
links = {}
for pid, _, _ in POSTS:
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", json={"status": "publish"}, auth=A, timeout=60).json()
    links[pid] = r.get("link"); print("PUBLISH", pid, r.get("status"), r.get("link"), flush=True)
    subprocess.run([PY, os.path.join(ROOT, "tools", "google_indexing.py"), r.get("link")], cwd=ROOT)
for i, (pid, text, tags) in enumerate(POSTS):
    if i: time.sleep(180)
    print("X", pid, time.strftime("%H:%M:%S"), flush=True)
    subprocess.run([PY, os.path.join(ROOT, "tools", "x_auto_post_buffer.py"), "--text", text, "--hashtags", tags,
                    "--post-id", str(pid), "--url", links[pid]], cwd=ROOT)
print("DONE", flush=True)
