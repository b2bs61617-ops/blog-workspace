import json, base64, urllib.request
REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"')
def api(key, path, body=None, method=None):
    base = env[f"WP_{key}_URL"].rstrip("/")
    auth = base64.b64encode(f"{env[f'WP_{key}_USERNAME']}:{env[f'WP_{key}_APP_PASSWORD']}".encode()).decode()
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method=method or ("POST" if data else "GET"))
    req.add_header("Authorization", "Basic " + auth)
    if data: req.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(req).read().decode())
