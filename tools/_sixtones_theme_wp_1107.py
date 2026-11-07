# -*- coding: utf-8 -*-
"""Apply SixTONES member colors (tools/sixtones_theme.py) to existing chomoand-0.com posts in place (2026-11-07).
Raw content is backed up to backups/chomoand0_membercolor_2026-11-07/{id}.html before updating."""
import os, sys, json, base64, urllib.request
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import sixtones_theme as st

JOBS = {1347: None, 1331: None, 1307: None, 1284: "松村北斗", 1175: "松村北斗", 1150: "松村北斗"}  # None = per-section
BK = os.path.join(REPO, "backups", "chomoand0_membercolor_2026-11-07")
env = {}
for l in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); env[k.strip()] = v.strip().strip('"')
B = env["WP_AUDITION_URL"].rstrip("/")
A = base64.b64encode(f"{env['WP_AUDITION_USERNAME']}:{env['WP_AUDITION_APP_PASSWORD']}".encode()).decode()

def req(path, data=None):
    r = urllib.request.Request(B + path, data=data, method="POST" if data else "GET")
    r.add_header("Authorization", "Basic " + A)
    if data: r.add_header("Content-Type", "application/json")
    return json.load(urllib.request.urlopen(r, timeout=120))

for pid, member in JOBS.items():
    p = req(f"/wp-json/wp/v2/posts/{pid}?context=edit")
    raw = p["content"]["raw"]
    open(os.path.join(BK, f"{pid}.html"), "w", encoding="utf-8").write(raw)
    new = st.apply_theme(raw, member) if member else st.per_section(raw)
    if new == raw:
        print(pid, "no change"); continue
    req(f"/wp-json/wp/v2/posts/{pid}", json.dumps({"content": new}).encode())
    left = sum(new.count(c) for c in st.NEUTRAL.values())
    print(pid, p["status"], member or "per-section", "neutral left:", left)
