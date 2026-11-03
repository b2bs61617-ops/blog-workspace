"""WPの記事をキーワード検索して id/status/link/title を出す(相互リンク確認用)。usage: python tools/_wp_find.py SITEPREFIX 検索語..."""
import sys, json, base64, urllib.request, urllib.parse, html
env = {}
for l in open(".env", encoding="utf-8"):
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); env[k.strip()] = v.strip().strip('"')
P = sys.argv[1]
B = env[f"WP_{P}_URL"].rstrip("/")
A = base64.b64encode(f"{env[f'WP_{P}_USERNAME']}:{env[f'WP_{P}_APP_PASSWORD']}".encode()).decode()
for q in sys.argv[2:]:
    u = f"{B}/wp-json/wp/v2/posts?search={urllib.parse.quote(q)}&status=publish,draft&per_page=10&_fields=id,status,link,title"
    r = urllib.request.Request(u, headers={"Authorization": "Basic " + A})
    for d in json.load(urllib.request.urlopen(r)):
        print(q, "|", d["id"], d["status"], d["link"], "|", html.unescape(d["title"]["rendered"]))
