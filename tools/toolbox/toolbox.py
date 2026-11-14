# -*- coding: utf-8 -*-
"""マツの道具箱(2026-11-14〜)。道具をボタンで動かす入口。マツ(Claude)がいなくても動く。

ダブルクリック: Windows = run.bat / Mac = run.command  → ブラウザに道具箱が開く(このPCの中だけで動く)。
    python tools/toolbox/toolbox.py              # 道具箱を開く
    python tools/toolbox/toolbox.py --doctor     # このPCで道具が動くか点検(足りないものと直し方を出す)
    python tools/toolbox/toolbox.py --install    # 足りないPythonの部品を入れる
    python tools/toolbox/toolbox.py --setup-ai   # パソコンに入れるAI(Ollama)のモデルを入れる
標準ライブラリだけで動く。Python 3.9対応。
"""
import importlib.util
import json
import os
import platform
import secrets
import shutil
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import blogkit  # noqa: E402

MODULES = [("requests", "requests", "外部AI・X投稿"), ("google.genai", "google-genai", "Gemini(外部AI)"),
           ("google.auth", "google-auth", "Search Console・Google通知")]
TOKEN = secrets.token_urlsafe(12)
JOBS = {}


# ---------------------------------------------------------------- 点検・準備
def ram_gb():
    try:
        if sys.platform == "win32":
            import ctypes

            class MS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + [
                    (n, ctypes.c_ulonglong) for n in ("ullTotalPhys", "ullAvailPhys", "ullTotalPageFile", "ullAvailPageFile",
                                                      "ullTotalVirtual", "ullAvailVirtual", "sullAvailExtendedVirtual")]
            ms = MS()
            ms.dwLength = ctypes.sizeof(MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms))
            return ms.ullTotalPhys / 2 ** 30
        if sys.platform == "darwin":
            return int(subprocess.check_output(["sysctl", "-n", "hw.memsize"]).strip()) / 2 ** 30
        for line in open("/proc/meminfo"):
            if line.startswith("MemTotal"):
                return int(line.split()[1]) / 2 ** 20
    except Exception:  # noqa: BLE001
        pass
    return 0


def recommend_model(gb):
    """メモリに合うモデル。小さいPCに大きいモデルを入れると固まるので控えめに選ぶ。"""
    return "gemma3:12b" if gb >= 24 else "gemma3:4b" if gb >= 7 else "gemma3:1b"


def find_ollama():
    exe = shutil.which("ollama")
    if exe:
        return exe
    for p in (os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe"), "/opt/homebrew/bin/ollama", "/usr/local/bin/ollama"):
        if os.path.exists(p):
            return p
    return None


def ollama_models():
    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2) as r:
            return [m["name"] for m in json.loads(r.read().decode())["models"]]
    except Exception:  # noqa: BLE001
        return None


def doctor():
    ok = True
    print("PC: {} / {} / Python {} / メモリ {:.0f}GB".format(platform.node(), platform.system(), sys.version.split()[0], ram_gb()))
    if sys.version_info < (3, 9):
        ok = False
        print("  × Pythonが古い(3.9以上が要る)")
    missing = [(pip, use) for mod, pip, use in MODULES if not _has(mod)]
    for pip, use in missing:
        print("  △ {} が無い({}が使えない)".format(pip, use))
    if missing:
        print("    → 直し方: 道具箱の「足りない部品を入れる」ボタン(または python tools/toolbox/toolbox.py --install)")
    else:
        print("  ○ Pythonの部品はそろっている")
    print("--- サイトの鍵と接続")
    if blogkit._check() != 0:
        ok = False
        print("    → 鍵が足りないサイトは下書き投稿・公開ができない(読むだけの道具は動く)。鍵はトモキに聞いてワン")
    print("--- パソコンに入れるAI(無くても道具は動く。無料枠が切れたとき・ネットが無いときの予備)")
    exe, models = find_ollama(), ollama_models()
    rec = recommend_model(ram_gb())
    if not exe:
        how = "winget install Ollama.Ollama" if sys.platform == "win32" else "brew install ollama" if sys.platform == "darwin" else "https://ollama.com/download"
        print("  △ Ollamaが入っていない → 入れるなら: {}\n    そのあと: python tools/toolbox/toolbox.py --setup-ai(このPCのおすすめ: {})".format(how, rec))
    elif models is None:
        print("  △ Ollamaは入っているが動いていない → 「ollama serve」で起動(Macは brew services start ollama)")
    elif not models:
        print("  △ モデルが入っていない → python tools/toolbox/toolbox.py --setup-ai(おすすめ: {})".format(rec))
    else:
        print("  ○ 使える: " + ", ".join(models))
    print("\n点検おわり:", "道具は動くワン" if ok else "上の × と鍵の不足を直してワン")
    return 0 if ok else 1


def _has(mod):
    try:
        return importlib.util.find_spec(mod) is not None
    except (ImportError, ValueError):
        return False


def install():
    need = [pip for mod, pip, _ in MODULES if not _has(mod)]
    if not need:
        print("足りない部品は無いワン")
        return 0
    print("入れる:", " ".join(need))
    return subprocess.call([sys.executable, "-m", "pip", "install", "--user"] + need)


def setup_ai():
    exe = find_ollama()
    if not exe:
        print("Ollamaが入っていないワン。先に入れてから、もう一度これを実行してワン(入れ方は --doctor に出る)")
        return 1
    if ollama_models() is None:
        print("Ollamaを起動するワン…")
        flags = {"creationflags": 0x08000000} if sys.platform == "win32" else {}
        subprocess.Popen([exe, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **flags)
        import time
        time.sleep(5)
    model = recommend_model(ram_gb())
    have = ollama_models() or []
    if model in have:
        print("もう入っているワン:", model)
        return 0
    print("モデル {} を入れるワン(数GBあるので時間がかかる)…".format(model), flush=True)
    return subprocess.call([exe, "pull", model])


# ---------------------------------------------------------------- 道具の実行
def _py(script, *args):
    return [sys.executable, "-u", str(TOOLS / script)] + [str(a) for a in args if a not in (None, "")]


def _opt(flag, value):
    value = (value or "").strip()
    return [flag, value] if value else []


def build_command(tool, q):
    """画面からの入力を、決まった形のコマンドにする(自由なコマンドは受け付けない)。"""
    site = q.get("site", "")
    if site and site not in blogkit.SITES:
        raise ValueError("サイト名がちがう")
    pid = q.get("post_id", "").strip()
    if pid and not pid.isdigit():
        raise ValueError("記事IDは数字で入れる")
    if tool == "fact":
        if not (site and pid):
            raise ValueError("サイトと記事IDを入れる")
        return _py("fact_check.py", "--site", site, "--post-id", pid, *_opt("--names", q.get("names")),
                   None if q.get("net") else "--no-net", "--ai" if q.get("ai") else None)
    if tool == "nobishiro":
        return _py("nobishiro/nobishiro.py", *(["--site", site] if site else []), "--links" if q.get("links") else None)
    if tool == "neta":
        days = q.get("days", "35")
        return _py("neta_calendar/neta_calendar.py", "--days", days if days.isdigit() else "35", *(["--site", site] if site else []))
    if tool == "xpost":
        if not (site and pid):
            raise ValueError("サイトと記事IDを入れる")
        return _py("xpost_ideas.py", "--site", site, "--post-id", pid, *_opt("--hide", q.get("hide")))
    if tool == "xcheck":
        if not q.get("text", "").strip():
            raise ValueError("本文を入れる")
        return _py("xpost_ideas.py", "check", "--text", q["text"], *_opt("--tags", q.get("tags")), *_opt("--hide", q.get("hide")))
    if tool == "suggest":
        name = q.get("name", "").strip()
        if not name:
            raise ValueError("名前を入れる")
        return _py("suggest-finder/suggest_finder.py", name, *(["--max", "50"] if q.get("quick") else []))
    if tool in ("doctor", "install", "setup-ai"):
        return [sys.executable, "-u", str(Path(__file__).resolve()), "--" + tool]
    raise ValueError("知らない道具")


def start_job(cmd):
    jid = secrets.token_hex(6)
    job = {"out": [], "done": False, "code": None}
    JOBS[jid] = job
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")

    def work():
        try:
            p = subprocess.Popen(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env,
                                 text=True, encoding="utf-8", errors="replace")
            for line in p.stdout:
                job["out"].append(line)
            job["code"] = p.wait()
        except Exception as e:  # noqa: BLE001
            job["out"].append("動かせなかった: {}\n".format(e))
            job["code"] = -1
        job["done"] = True

    threading.Thread(target=work, daemon=True).start()
    return jid


PAGE = """<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>マツの道具箱</title><style>
body{font-family:system-ui,sans-serif;margin:0;padding:16px;background:#f6f7f9;color:#222;line-height:1.6;max-width:860px;margin:auto}
h1{font-size:1.4em}.card{background:#fff;border-radius:10px;padding:14px 16px;margin:12px 0;box-shadow:0 1px 3px rgba(0,0,0,.1)}
.card h2{font-size:1.1em;margin:0 0 4px}.sub{color:#666;font-size:.9em;margin:0 0 8px}
input,select,textarea{font-size:1em;padding:6px;margin:3px 6px 3px 0;border:1px solid #bbb;border-radius:6px;max-width:100%}
button{font-size:1em;padding:8px 18px;border:0;border-radius:8px;background:#c2410c;color:#fff;font-weight:bold;cursor:pointer;margin-top:6px}
button:disabled{background:#999}button.sm{background:#555;padding:5px 12px;font-weight:normal}
pre{background:#111;color:#e6e6e6;padding:12px;border-radius:8px;white-space:pre-wrap;word-break:break-all;max-height:60vh;overflow:auto;font-size:.88em}
label{white-space:nowrap}@media(prefers-color-scheme:dark){body{background:#16181c;color:#e6e6e6}.card{background:#22252b}.sub{color:#aaa}
input,select,textarea{background:#16181c;color:#e6e6e6;border-color:#555}}</style></head><body>
<h1>🐕 マツの道具箱</h1><p class="sub">ボタンを押すと、このパソコンの中で道具が動く。記事を書き換えたり公開したりはしない(読むだけ)。</p>

<div class="card"><h2>① 投稿前の事実チェック</h2><p class="sub">下書きの日付と曜日・名前の字・年齢・さん付け・読みにくい文・リンク切れを調べる。</p>
<form data-tool="fact">__SITES__ <input name="post_id" placeholder="記事ID" size="8" inputmode="numeric">
<input name="names" placeholder="メンバー以外の人名(カンマ区切り)" size="28"><br>
<label><input type="checkbox" name="net" checked> リンク切れも調べる</label> <label><input type="checkbox" name="ai"> AIに食いちがいも聞く</label><br>
<button>調べる</button></form></div>

<div class="card"><h2>② 伸びしろ診断</h2><p class="sub">公開ずみの記事を全部読み、直す順番つきのリストを作る。終わると結果のページが開く(数分)。</p>
<form data-tool="nobishiro">__SITES_ALL__ <label><input type="checkbox" name="links"> 動画・Xのリンク切れも調べる(+10〜20分)</label><br>
<button>診断する</button></form></div>

<div class="card"><h2>③ ネタ先読みカレンダー</h2><p class="sub">誕生日・行事・毎週の番組から「今週書く」「来週書く」を出す。</p>
<form data-tool="neta">__SITES_ALL__ <label>先 <input name="days" value="35" size="3" inputmode="numeric"> 日ぶん</label><br><button>出す</button></form></div>

<div class="card"><h2>④ X投稿文の案出し</h2><p class="sub">いまのルール(答えは隠す・誘導なし)で案を作り、ルール違反の案は自動で落とす。</p>
<form data-tool="xpost">__SITES__ <input name="post_id" placeholder="記事ID" size="8" inputmode="numeric">
<input name="hide" placeholder="隠す答え(ブランド名・店名など、カンマ区切り)" size="34"><br><button>案を出す</button></form>
<p class="sub" style="margin-top:12px">自分で書いた文がルールに合うかだけ調べる:</p>
<form data-tool="xcheck"><textarea name="text" rows="3" cols="46" placeholder="投稿の本文"></textarea><br>
<input name="tags" placeholder="#SnowMan #目黒蓮" size="26"> <input name="hide" placeholder="隠す答え" size="16"><br><button class="sm">文を調べる</button></form></div>

<div class="card"><h2>⑤ サジェスト穴場ファインダー</h2><p class="sub">名前を入れると、ライバルの少ない検索キーワードを探す(全部で約45分。別の画面に結果が開く)。</p>
<form data-tool="suggest"><input name="name" placeholder="調べたい名前" size="18"> <label><input type="checkbox" name="quick"> 急ぎ(約5分)</label><br>
<button>探す</button></form></div>

<div class="card"><h2>このパソコンの点検</h2><p class="sub">道具が動く準備ができているかを調べる。足りないものと直し方が出る。</p>
<form data-tool="doctor" style="display:inline"><button class="sm">点検する</button></form>
<form data-tool="install" style="display:inline"><button class="sm">足りない部品を入れる</button></form>
<form data-tool="setup-ai" style="display:inline"><button class="sm">パソコンに入れるAIのモデルを入れる</button></form></div>

<div class="card"><h2>結果</h2><pre id="out">ここに結果が出るワン</pre></div>
<script>
var T="__TOKEN__",out=document.getElementById('out'),busy=false;
document.querySelectorAll('form').forEach(function(f){f.onsubmit=function(e){e.preventDefault();if(busy)return;
 var q=new URLSearchParams(new FormData(f));q.set('tool',f.dataset.tool);q.set('t',T);busy=true;lock(true);out.textContent='動かしているワン…\\n';
 fetch('/run',{method:'POST',body:q}).then(function(r){return r.json()}).then(function(j){
  if(j.error){out.textContent='できなかった: '+j.error;busy=false;lock(false);return}poll(j.id)}).catch(function(x){out.textContent='道具箱が止まっているみたい。run をもう一度ダブルクリックしてワン';busy=false;lock(false)})}});
function lock(b){document.querySelectorAll('button').forEach(function(x){x.disabled=b})}
function poll(id){fetch('/job?id='+id+'&t='+T).then(function(r){return r.json()}).then(function(j){out.textContent=j.out||'動かしているワン…';out.scrollTop=out.scrollHeight;
 if(j.done){busy=false;lock(false);out.textContent+='\\n(おわり)'}else setTimeout(function(){poll(id)},1000)})}
</script></body></html>"""


def page():
    opts = "".join('<option value="{}">{}</option>'.format(k, s["label"]) for k, s in blogkit.SITES.items())
    return (PAGE.replace("__SITES_ALL__", '<select name="site"><option value="">全サイト</option>{}</select>'.format(opts))
            .replace("__SITES__", '<select name="site">{}</select>'.format(opts)).replace("__TOKEN__", TOKEN))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, body, ctype="application/json", code=200):
        data = body.encode("utf-8") if isinstance(body, str) else json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        if u.path == "/":
            return self._send(page(), "text/html")
        if u.path == "/job" and q.get("t") == TOKEN and q.get("id") in JOBS:
            j = JOBS[q["id"]]
            return self._send({"out": "".join(j["out"])[-20000:], "done": j["done"], "code": j["code"]})
        self._send({"error": "not found"}, code=404)

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        q = {k: v[0] for k, v in parse_qs(self.rfile.read(n).decode("utf-8")).items()}
        if urlparse(self.path).path != "/run" or q.get("t") != TOKEN:
            return self._send({"error": "forbidden"}, code=403)
        try:
            cmd = build_command(q.get("tool", ""), q)
        except ValueError as e:
            return self._send({"error": str(e)})
        self._send({"id": start_job(cmd)})


def serve(open_browser=True):
    srv = None
    for port in range(8765, 8785):
        try:
            srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            continue
    if srv is None:
        print("道具箱を開けなかった(ポートが空いていない)")
        return 1
    url = "http://127.0.0.1:{}/".format(srv.server_address[1])
    print("マツの道具箱を開いたワン: {}\nこの黒い画面は開いたままにしてワン(閉じると道具箱も止まる)".format(url), flush=True)
    if open_browser:
        webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit({"--doctor": doctor, "--install": install, "--setup-ai": setup_ai}.get(arg, lambda: serve("--no-open" not in sys.argv))())
