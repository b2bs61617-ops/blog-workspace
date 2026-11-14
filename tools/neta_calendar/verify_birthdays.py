# -*- coding: utf-8 -*-
"""名簿(tools/data/members.json)の誕生日を、Wikipedia日本語版で確かめて埋める。

マツの記憶で誕生日を書かないための道具。birthdayがnullの人だけ埋め、すでに入っている人は見くらべて
食いちがいを知らせる(書き換えない)。グループ名がページに出てこない人(同姓同名の別人)は埋めない。

usage: python tools/neta_calendar/verify_birthdays.py [--dry-run] [--recheck(入っている人も見くらべる)]
"""
import datetime
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

MEMBERS = Path(__file__).resolve().parent.parent / "data" / "members.json"
API = "https://ja.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvslots=main&redirects=1&format=json&titles="
SUFFIXES = ("", " (アイドル)", " (タレント)", " (歌手)", " (ジャニーズ)")


def parse_birthday(wikitext):
    """ウィキテキストから生年月日を取り出す。見つからなければ None。"""
    m = re.search(r"\{\{\s*生年月日と年齢\s*\|\s*(\d{4})\s*\|\s*(\d{1,2})\s*\|\s*(\d{1,2})", wikitext)
    if not m:
        y = re.search(r"\|\s*生年\s*=\s*(\d{4})", wikitext)
        mo = re.search(r"\|\s*生月\s*=\s*(\d{1,2})", wikitext)
        d = re.search(r"\|\s*生日\s*=\s*(\d{1,2})", wikitext)
        if not (y and mo and d):
            return None
        parts = (y.group(1), mo.group(1), d.group(1))
    else:
        parts = m.groups()
    try:
        return str(datetime.date(*map(int, parts)))
    except ValueError:
        return None


def fetch(title):
    req = urllib.request.Request(API + urllib.parse.quote(title), headers={"User-Agent": "blog-workspace-toolbox/1.0"})
    for wait in (2, 20, 60):  # 続けて聞くと断られる(429)ので、間をあけて聞く
        time.sleep(wait)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                pages = json.loads(r.read().decode("utf-8"))["query"]["pages"]
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or wait == 60:
                raise
    for p in pages.values():
        if "revisions" in p:
            return p["revisions"][0]["slots"]["main"]["*"]
    return None


def lookup(name, group_words):
    for suf in SUFFIXES:
        text = fetch(name + suf)
        if text and any(w in text for w in group_words):
            b = parse_birthday(text)
            if b:
                return b, name + suf
    return None, None


def main():
    dry = "--dry-run" in sys.argv
    raw = MEMBERS.read_text(encoding="utf-8")
    groups = json.loads(raw)["groups"]
    today = datetime.date.today()
    for conf in groups.values():
        words = [conf["label"]] + conf.get("aliases", [])
        for m in conf["members"]:
            if m.get("birthday") and "--recheck" not in sys.argv:
                continue
            query = m.get("wiki") or m["name"]
            try:
                found, page = lookup(query, words)
            except Exception as e:  # noqa: BLE001
                print("  {}: 調べられなかった({})".format(m["name"], str(e)[:50]))
                continue
            if not found:
                print("  {}: 見つからない(要確認のまま)".format(m["name"]))
            elif m.get("birthday") and m["birthday"] != found:
                print("  {}: 名簿は{}、Wikipediaは{} → 食いちがい。人が確かめる".format(m["name"], m["birthday"], found))
            elif m.get("birthday"):
                print("  {}: {} 一致".format(m["name"], found))
            else:
                print("  {}: {} を記入(出どころ: Wikipedia「{}」)".format(m["name"], found, page))
                old = re.search(r'\{"name": "%s"[^\n]*' % re.escape(m["name"]), raw)
                if old and '"birthday": null' in old.group(0):
                    new = old.group(0).replace('"birthday": null', '"birthday": "{}", "source": "Wikipedia日本語版「{}」({}確認)"'
                                               .format(found, page, today))
                    raw = raw.replace(old.group(0), new)
    if not dry:
        MEMBERS.write_text(raw, encoding="utf-8")
        print("名簿を更新したワン")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
