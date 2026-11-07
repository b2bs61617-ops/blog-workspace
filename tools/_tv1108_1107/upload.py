import json, base64, urllib.request, shutil
REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"')
def api(key, path, body=None):
    base = env[f"WP_{key}_URL"].rstrip("/")
    auth = base64.b64encode(f"{env[f'WP_{key}_USERNAME']}:{env[f'WP_{key}_APP_PASSWORD']}".encode()).decode()
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method="POST" if data else "GET")
    req.add_header("Authorization", "Basic " + auth)
    if data: req.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(req).read().decode())
for key,pid,fn in [("CHOMO4",2348,"travis_japan"),("CHOMO2",523,"snowman"),("AUDITION",1292,"sixtones"),("CHOMO5",582,"key_to_lit")]:
    cur = api(key, f"/wp-json/wp/v2/posts/{pid}?context=edit")["content"]["raw"]
    assert cur == open(f"wp_{pid}.html",encoding="utf-8").read(), f"{pid} changed on WP since fetch"
    new = open(f"new_{pid}.html",encoding="utf-8").read()
    r = api(key, f"/wp-json/wp/v2/posts/{pid}", {"content": new})
    shutil.copy(f"new_{pid}.html", REPO + rf"\articles\{fn}_tv_schedule_1108_1114.html")
    print(key, pid, r["status"], r["title"]["raw"], r["modified"], r["link"])
