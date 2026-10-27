"""全サイトのアナリティクス(PV)とアドセンス(収益)を1ページにまとめてスマホで見るためのスクリプト。

chomoand-3.moe(記事なし・広告なし)にパスワード付き固定ページを作り、実行のたびに中身を最新の数字で上書きする。
タスクスケジューラで1時間おきに実行する想定(install_task.bat)。

認証:
  - アナリティクス: Indexing用サービスアカウント(.envのGOOGLE_INDEXING_CREDENTIALS_PATH)。
    5サイトのGA4アカウントに「閲覧者」として追加済み(2026-10-19)。
  - アドセンス: サービスアカウント非対応のため、トモキのOAuth許可で得たトークン
    (G:\\マイドライブ\\ブログ関係\\adsense-token.json、adsense_auth.pyで発行)。
  - WordPress: .envのWP_CHOMO3_*。

ページIDと合言葉は G:\\マイドライブ\\ブログ関係\\site-dashboard.json に保存(初回実行で自動作成)。

実行:
  python tools/site-dashboard/site_dashboard.py            # 集計してページを更新
  python tools/site-dashboard/site_dashboard.py --dry-run  # 集計結果を表示するだけ(ページは触らない)
"""
import argparse
import html
import json
import secrets
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from google.auth.transport.requests import AuthorizedSession, Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

ROOT = Path(__file__).resolve().parent.parent.parent
DRIVE_DIR = Path(r"G:\マイドライブ\ブログ関係")
ADSENSE_TOKEN_FILE = DRIVE_DIR / "adsense-token.json"
STATE_FILE = DRIVE_DIR / "site-dashboard.json"
JST = timezone(timedelta(hours=9))
PAGE_SLUG = "mypage-stats"
PAGE_TITLE = "ブログ集計"

# (表示名, AdSenseのドメイン名, GA4プロパティID, 色)
SITES = [
    ("トレンド", "chomoand.com", "473419828", "#e8743b"),
    ("KO1KEYZ", "chomoand-1.com", "522443997", "#d6336c"),
    ("Snow Man", "chomoand-2.com", "552989311", "#4a90d9"),
    ("SixTONES", "chomoand-0.com", "541752057", "#555555"),
    ("トラジャ", "chomoand-4.blog", "551881009", "#8e5ad6"),
    ("キテレツ", "chomoand-5.site", "552198888", "#2f9e77"),
]

GA_RANGES = [
    ("today", "today", "today"),
    ("yesterday", "yesterday", "yesterday"),
    ("week", "7daysAgo", "yesterday"),
    ("month", None, "today"),  # startは月初(実行時に決める)
]
AD_RANGES = ["TODAY", "YESTERDAY", "LAST_7_DAYS", "MONTH_TO_DATE"]
AD_KEYS = dict(zip(AD_RANGES, ["today", "yesterday", "week", "month"]))


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


# ---------- アナリティクス ----------

def ga_session(env):
    creds = service_account.Credentials.from_service_account_file(
        env["GOOGLE_INDEXING_CREDENTIALS_PATH"],
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )
    return AuthorizedSession(creds)


def strip_site_name(title):
    """「記事タイトル | サイト名」からサイト名を外す(スマホで幅を取るため)。"""
    return title.rsplit(" | ", 1)[0]


def fetch_ga(session, property_id, month_start):
    """PV/訪問者を4期間ぶん + 今見ている人数 + 今日の人気記事TOP3を返す。"""
    base = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}"
    ranges = [
        {"name": name, "startDate": start or month_start, "endDate": end}
        for name, start, end in GA_RANGES
    ]
    r = session.post(f"{base}:runReport", json={
        "dateRanges": ranges,
        "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}],
    }, timeout=60)
    r.raise_for_status()
    out = {name: {"pv": 0, "users": 0} for name, _, _ in GA_RANGES}
    for row in r.json().get("rows", []):
        name = row["dimensionValues"][0]["value"]
        pv, users = (int(m["value"]) for m in row["metricValues"])
        out[name] = {"pv": pv, "users": users}

    rt = session.post(f"{base}:runRealtimeReport", json={
        "metrics": [{"name": "activeUsers"}],
    }, timeout=60)
    rt.raise_for_status()
    rows = rt.json().get("rows", [])
    out["now"] = int(rows[0]["metricValues"][0]["value"]) if rows else 0

    top = session.post(f"{base}:runReport", json={
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [{"name": "pageTitle"}],
        "metrics": [{"name": "screenPageViews"}],
        "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
        "limit": 3,
    }, timeout=60)
    top.raise_for_status()
    out["top"] = [
        (strip_site_name(row["dimensionValues"][0]["value"]), int(row["metricValues"][0]["value"]))
        for row in top.json().get("rows", [])
    ]
    return out


# ---------- アドセンス ----------

def adsense_session():
    creds = Credentials.from_authorized_user_file(str(ADSENSE_TOKEN_FILE))
    if not creds.valid:
        creds.refresh(Request())
    return AuthorizedSession(creds)


def normalize_domain(domain):
    return domain.lower().removeprefix("www.")


def fetch_adsense(session):
    """{ドメイン: {today/yesterday/week/month: 収益(円)}} を返す。"""
    accounts = session.get("https://adsense.googleapis.com/v2/accounts", timeout=60)
    accounts.raise_for_status()
    account = accounts.json()["accounts"][0]["name"]
    out = {}
    for date_range in AD_RANGES:
        r = session.get(
            f"https://adsense.googleapis.com/v2/{account}/reports:generate",
            params={
                "dateRange": date_range,
                "dimensions": "DOMAIN_NAME",
                "metrics": ["ESTIMATED_EARNINGS"],
                "currencyCode": "JPY",
            },
            timeout=60,
        )
        r.raise_for_status()
        for row in r.json().get("rows", []):
            domain = normalize_domain(row["cells"][0]["value"])
            earnings = float(row["cells"][1]["value"])
            out.setdefault(domain, {})[AD_KEYS[date_range]] = earnings
    return out


# ---------- ページ生成 ----------

def yen(v):
    return "-" if v is None else f"¥{round(v):,}"


def num(v):
    return f"{v:,}"


def build_html(results, adsense, updated_at, errors):
    esc = html.escape
    keys = ["today", "yesterday", "week", "month"]
    total = {k: 0 for k in keys}
    total_ad = {k: 0.0 for k in keys}
    total_now = 0
    cards = []
    for label, domain, _, color in SITES:
        ga = results.get(domain)
        ad = adsense.get(domain, {}) if adsense is not None else None
        if ga:
            for k in keys:
                total[k] += ga[k]["pv"]
            total_now += ga["now"]
        if ad:
            for k in keys:
                total_ad[k] += ad.get(k, 0.0)

        def pv(k):
            return num(ga[k]["pv"]) if ga else "取得失敗"

        def money(k):
            if ad is None:
                return "取得失敗"
            return yen(ad.get(k)) if ad.get(k) else "¥0"

        top_html = ""
        if ga and ga["top"]:
            items = "".join(
                f'<li><span class="sd-t">{esc(title)}</span><b>{num(v)}</b></li>'
                for title, v in ga["top"]
            )
            top_html = f'<details class="sd-top"><summary>今日の人気記事</summary><ol>{items}</ol></details>'

        now_html = f'<span class="sd-now">● 今 {ga["now"]}人</span>' if ga else ""
        cards.append(
            f'<section class="sd-card" style="border-top:4px solid {color}">'
            f'<div class="sd-head"><b>{esc(label)}</b><small>{esc(domain)}</small>{now_html}</div>'
            f'<table class="sd-tbl"><tr><th></th><th>今日</th><th>昨日</th><th>7日</th><th>今月</th></tr>'
            f'<tr><td>PV</td>{"".join(f"<td>{pv(k)}</td>" for k in keys)}</tr>'
            f'<tr><td>収益</td>{"".join(f"<td>{money(k)}</td>" for k in keys)}</tr></table>'
            f"{top_html}</section>"
        )

    ad_ok = adsense is not None
    summary = (
        '<section class="sd-sum">'
        f'<div><small>今日のPV</small><b>{num(total["today"])}</b></div>'
        f'<div><small>今日の収益</small><b>{yen(total_ad["today"]) if ad_ok else "-"}</b></div>'
        f'<div><small>今月の収益</small><b>{yen(total_ad["month"]) if ad_ok else "-"}</b></div>'
        f'<div><small>今見ている人</small><b>{num(total_now)}</b></div>'
        "</section>"
    )
    err_html = ""
    if errors:
        err_html = '<p class="sd-err">⚠ ' + "<br>".join(esc(e) for e in errors) + "</p>"

    style = (
        "<style>"
        ".sd{font-family:-apple-system,'Hiragino Sans','Noto Sans JP',sans-serif;color:#222;max-width:640px;margin:0 auto}"
        ".sd *{box-sizing:border-box}"
        ".sd-upd{font-size:13px;color:#666;margin:0 0 12px}"
        ".sd-sum{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px}"
        ".sd-sum div{background:#f4f1fa;border-radius:12px;padding:10px 12px}"
        ".sd-sum small{display:block;font-size:12px;color:#666}"
        ".sd-sum b{font-size:22px}"
        ".sd-card{background:#fff;border:1px solid #e5e5e5;border-radius:12px;padding:10px 12px;margin-bottom:12px}"
        ".sd-head{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin-bottom:6px}"
        ".sd-head b{font-size:17px}.sd-head small{color:#888;font-size:12px}"
        ".sd-now{margin-left:auto;font-size:12px;color:#2f9e44}"
        ".sd-tbl{width:100%;border-collapse:collapse;font-size:14px;margin:0!important;table-layout:fixed}"
        ".sd-tbl th,.sd-tbl td{border:none!important;padding:4px 2px!important;text-align:right;background:none!important;white-space:nowrap}"
        ".sd-tbl th{font-size:12px;color:#888;font-weight:normal}"
        ".sd-tbl td:first-child,.sd-tbl th:first-child{text-align:left;color:#666;font-size:12px;width:3.2em}"
        ".sd-top{margin-top:6px;font-size:13px}.sd-top summary{color:#666;cursor:pointer}"
        ".sd-top ol{margin:6px 0 0;padding-left:1.4em}.sd-top li{display:flex;gap:6px;margin-bottom:4px}"
        ".sd-t{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}"
        ".sd-err{background:#fff3f0;color:#c0392b;font-size:13px;padding:8px;border-radius:8px}"
        ".sd-note{font-size:12px;color:#888}"
        "</style>"
    )
    body = (
        f'<div class="sd">{style}'
        f'<p class="sd-upd">最終更新 {updated_at:%m/%d %H:%M}(1時間おきに自動更新)</p>'
        f"{err_html}{summary}{''.join(cards)}"
        '<p class="sd-note">PVはアナリティクス、収益はアドセンスの見積もり額。収益は数時間遅れで反映されるワン。</p>'
        "</div>"
    )
    # wp:htmlブロックで包むと、WordPressが勝手に<p>や<br>を足さない
    return f"<!-- wp:html -->{body}<!-- /wp:html -->"


# ---------- WordPress ----------

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def publish_page(env, content, state):
    base = env["WP_CHOMO3_URL"].rstrip("/") + "/wp-json/wp/v2/pages"
    auth = (env["WP_CHOMO3_USERNAME"], env["WP_CHOMO3_APP_PASSWORD"])
    if not state.get("password"):
        state["password"] = secrets.token_urlsafe(6)
    payload = {
        "title": PAGE_TITLE,
        "slug": PAGE_SLUG,
        "status": "publish",
        "password": state["password"],
        "content": content,
        "comment_status": "closed",
        "meta": {"ssp_meta_robots": "noindex,nofollow"},
    }
    page_id = state.get("page_id")
    if page_id:
        r = requests.post(f"{base}/{page_id}", json=payload, auth=auth, timeout=60)
        if r.status_code == 404:
            page_id = None
    if not page_id:
        r = requests.post(base, json=payload, auth=auth, timeout=60)
    if r.status_code == 400 and "meta" in r.text:
        # SEO SIMPLE PACKのmetaがRESTで受け付けられない場合はmeta無しで再送
        payload.pop("meta")
        url = f"{base}/{page_id}" if page_id else base
        r = requests.post(url, json=payload, auth=auth, timeout=60)
    r.raise_for_status()
    data = r.json()
    state["page_id"] = data["id"]
    state["url"] = data["link"]
    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    env = load_env(ROOT / ".env")
    now = datetime.now(JST)
    month_start = now.strftime("%Y-%m-01")
    errors = []

    ga = ga_session(env)
    results = {}
    for label, domain, property_id, _ in SITES:
        try:
            results[domain] = fetch_ga(ga, property_id, month_start)
        except Exception as e:  # 1サイトの失敗で全体を止めない
            errors.append(f"{label}のアナリティクス取得に失敗: {e}")

    try:
        adsense = fetch_adsense(adsense_session())
    except Exception as e:
        adsense = None
        errors.append(f"アドセンス取得に失敗: {e}")

    if args.dry_run:
        print(json.dumps({"ga": results, "adsense": adsense, "errors": errors}, ensure_ascii=False, indent=2))
        return

    content = build_html(results, adsense, now, errors)
    state = publish_page(env, content, load_state())
    save_state(state)
    print(f"更新したワン: {state['url']}")
    for e in errors:
        print("警告:", e, file=sys.stderr)


if __name__ == "__main__":
    main()
