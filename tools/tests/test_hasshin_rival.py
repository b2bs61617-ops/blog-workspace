# -*- coding: utf-8 -*-
"""ライバルブログ見張り / 毎日の発信あつめ の純粋関数のテスト(通信・ブラウザは使わない)。"""
import datetime
import json

import hasshin as hs
import rival_watch as rw
import toolbox

UTC = datetime.timezone.utc
NOW = datetime.datetime(2026, 11, 14, 12, 0, tzinfo=UTC)

RSS = b"""<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>x</title>
<item><title>A &amp; B  old</title><link>https://e.com/a</link><pubDate>Thu, 12 Nov 2026 10:00:00 +0900</pubDate></item>
<item><title>new</title><link>https://e.com/b</link><pubDate>Sat, 14 Nov 2026 10:00:00 +0900</pubDate></item></channel></rss>"""
ATOM = b"""<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry><title>t1</title>
<link rel="alternate" href="https://e.com/1"/><link rel="replies" href="https://e.com/c"/><updated>2026-11-14T01:00:00Z</updated></entry></feed>"""
RDF = b"""<?xml version="1.0"?><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/"
xmlns:dc="http://purl.org/dc/elements/1.1/"><item><title>r1</title><link>https://e.com/r</link><dc:date>2026-11-13T09:00:00+09:00</dc:date></item></rdf:RDF>"""
YT = b"""<?xml version="1.0"?><feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns="http://www.w3.org/2005/Atom">
<entry><yt:videoId>abcdefghijk</yt:videoId><title>new video</title><link rel="alternate" href="https://www.youtube.com/watch?v=abcdefghijk"/>
<published>2026-11-14T03:00:00+00:00</published></entry></feed>"""
MEMBERS = {"snowman": {"label": "Snow Man", "aliases": ["スノーマン", "スノ"], "members": [{"name": "目黒蓮"}, {"name": "ラウール"}]},
           "ko1keyz": {"label": "KO1KEYZ", "aliases": ["コイキーズ"], "members": [{"name": "柳谷伊冴", "stage": "ISSA"}]}}


# ---------------- rival_watch
def test_parse_feed_three_formats_sorted_new_first():
    items = rw.parse_feed(RSS)
    assert [i["title"] for i in items] == ["new", "A & B old"] and items[0]["date"].tzinfo is not None
    assert rw.parse_feed(ATOM)[0]["url"] == "https://e.com/1"
    assert rw.parse_feed(RDF)[0]["date"] == datetime.datetime(2026, 11, 13, 0, 0, tzinfo=UTC)
    assert rw.parse_feed(b"<html>not a feed</html>") == [] and rw.parse_feed(b"broken<") == []


def test_parse_date_variants():
    assert rw.parse_date("2026-11-14T01:00:00.123Z") == datetime.datetime(2026, 11, 14, 1, 0, tzinfo=UTC)
    assert rw.parse_date("2026-11-14T10:00:00+0900").utcoffset() == datetime.timedelta(hours=9)
    assert rw.parse_date("") is None and rw.parse_date("きのう") is None


def test_parse_sitemap_index_and_urls():
    idx = (b'<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>https://e.com/page-sitemap.xml</loc></sitemap>'
           b"<sitemap><loc>https://e.com/post-sitemap2.xml</loc><lastmod>2026-11-14</lastmod></sitemap>"
           b"<sitemap><loc>https://e.com/post-sitemap1.xml</loc><lastmod>2026-01-01</lastmod></sitemap></sitemapindex>")
    assert rw.parse_sitemap(idx) == ("index", ["https://e.com/post-sitemap2.xml", "https://e.com/post-sitemap1.xml", "https://e.com/page-sitemap.xml"])
    kind, rows = rw.parse_sitemap(b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://e.com/a/</loc>'
                                  b"<lastmod>2026-11-14T09:00:00+09:00</lastmod></url></urlset>")
    assert kind == "urls" and rows[0]["url"] == "https://e.com/a/" and rows[0]["date"].year == 2026
    assert rw.parse_sitemap(b"<html/>") == ("", [])


def test_page_title_drops_site_name():
    assert rw.page_title("<title>目黒蓮のニットはどこの？値段も調査 | 推し活ブログ</title>") == "目黒蓮のニットはどこの？値段も調査"
    assert rw.page_title('<meta property="og:title" content="A &amp; B"><title>x</title>') == "A & B"


def test_feed_links_and_blog_key():
    html = ('<link rel="alternate" type="application/rss+xml" href="/feed/"><link rel="alternate" type="application/rss+xml" '
            'href="/comments/feed/"><link rel="stylesheet" href="a.css">')
    assert rw.feed_links(html, "https://e.com/x/") == ["https://e.com/feed/"]
    assert rw.blog_key("https://www.Example.com/a/b") == "example.com"
    assert rw.blog_key("https://ameblo.jp/someone/entry-1.html") == "ameblo.jp/someone"
    assert rw.blog_key("note.com/abc") == "note.com/abc"


def test_tag_title_and_ascii_stage_names():
    table = rw.name_table(MEMBERS)
    assert rw.tag_title("【Snow Man】目黒蓮の私服ニットはどこの？", table) == (["snowman"], ["目黒蓮"])
    assert rw.tag_title("KO1KEYZのISSAが着たシャツ", table) == (["ko1keyz"], ["柳谷伊冴"])
    assert rw.tag_title("MISSAという別の言葉", table) == ([], [])          # 英字の芸名は単語のときだけ
    assert rw.tag_title("スノーボードの話", table) == ([], [])              # 2文字の略称(スノ)は使わない


def test_topic_of_order():
    assert rw.topic_of("PV撮影の結婚式場はどこ？") == "ロケ地・お店"
    assert rw.topic_of("田中樹に熱愛？相手は誰") == "熱愛・結婚"
    assert rw.topic_of("目黒蓮は身長170cm？") == "学歴・家族"              # 「170cm」をCMと数えない
    assert rw.topic_of("新CMに出演決定") == "テレビ・出演"
    assert rw.topic_of("松田元太とおそろいの香水は？") == "私服・愛用品"
    assert rw.topic_of("ふつうの日記") == "そのほか"


def _p(blog, title, table):
    g, n = rw.tag_title(title, table)
    return {"blog": blog, "title": title, "groups": g, "members": n, "tokens": rw.tokens(title, [r[0] for r in table]),
            "topic": rw.topic_of(title), "date": NOW, "url": "https://" + blog + "/" + title[:4]}


def test_tokens_and_overlaps_need_two_blogs():
    table = rw.name_table(MEMBERS)
    assert rw.tokens("【Snow Man】目黒蓮のマルニのバッグまとめ", [r[0] for r in table]) == ["マルニ", "バッグ"]
    posts = [_p("a.com", "目黒蓮のマルニのバッグはどこの？", table), _p("b.com", "目黒蓮が持っていたマルニのトート", table),
             _p("a.com", "目黒蓮のマルニ2本目", table), _p("c.com", "ラウールのマルニ", table), _p("c.com", "ラウールの香水", table)]
    got = rw.find_overlaps(posts)
    assert len(got) == 1 and got[0]["who"] == {"目黒蓮"} and len(got[0]["posts"]) == 3 and "マルニ" in got[0]["tokens"]
    assert rw.find_overlaps([posts[0], posts[2]]) == []                   # 同じブログの2本は「かぶり」にしない
    assert dict(rw.topic_counts(posts))["私服・愛用品"] >= 2


def test_collect_drops_unrelated_posts_of_mixed_blogs(monkeypatch):
    table = rw.name_table(MEMBERS)
    feed = RSS.replace(b"new", "目黒蓮の指輪".encode("utf-8"))
    monkeypatch.setattr(rw, "fetch", lambda url, timeout=20: feed)
    mixed = {"name": "m", "url": "https://m.com/", "feed": "https://m.com/feed", "groups": ["snowman", "ko1keyz"]}
    only = {"name": "o", "url": "https://o.com/", "feed": "https://o.com/feed", "groups": ["snowman"]}
    state = {}
    posts, failed = rw.collect([mixed, only], table, 96, NOW, state)
    assert failed == [] and sorted((p["blog"], p["title"]) for p in posts) == [("m", "目黒蓮の指輪"), ("o", "A & B old"), ("o", "目黒蓮の指輪")]
    assert all(p["groups"] == ["snowman"] for p in posts) and state["https://m.com/feed"][0] == "https://e.com/b"
    again = rw.collect([only], table, 12, NOW, state)[0]                   # 2回目: 12時間以内の1本だけ、もう「見たことがある」
    assert [(p["title"], p["new"]) for p in again] == [("目黒蓮の指輪", False)]


def test_count_candidates_skips_big_media_and_own():
    results = [("snowman", "q1", [{"url": "https://fan.example.com/a", "title": "t"}, {"url": "https://news.yahoo.co.jp/x", "title": "y"},
                                  {"url": "https://chomoand-2.com/z", "title": "own"}]),
               ("travis", "q2", [{"url": "https://fan.example.com/b", "title": "t2"}, {"url": "https://ameblo.jp/u1/entry", "title": "a"}])]
    got = rw.count_candidates(results)
    assert got[0]["key"] == "fan.example.com" and got[0]["groups"] == ["snowman", "travis"] and len(got[0]["queries"]) == 2
    assert [c["key"] for c in got[1:]] == ["ameblo.jp/u1"]
    assert rw.count_candidates(results, ignore={"fan.example.com"})[0]["key"] == "ameblo.jp/u1"


def test_rivals_and_sources_files_are_valid():
    rivals = json.loads(rw.RIVALS.read_text(encoding="utf-8"))
    keys = [rw.blog_key(b["url"]) for b in rivals["blogs"]]
    assert len(keys) == len(set(keys)) and all(b["feed"].startswith("http") and b["groups"] for b in rivals["blogs"])
    assert not any(d in k for k in keys for d in rw.own_domains())
    sources = json.loads(hs.SOURCES.read_text(encoding="utf-8"))
    names = {m["name"] for g in rw.load_members().values() for m in g["members"]}
    for g, conf in sources["groups"].items():
        assert g in rw.load_members()
        for kind in ("x", "instagram"):
            for acc in conf[kind]:
                assert acc["handle"] and "checked" in acc and acc.get("member", next(iter(names))) in names


# ---------------- hasshin
def test_extract_and_pick_questions_have_no_author():
    assert hs.extract_questions("かわいい！このニットどこの？ https://t.co/x @abc 教えて") == ["このニットどこの？"]
    replies = [{"author": "だれか", "text": "このニットどこの？"}, {"author": "べつの人", "text": "この ニットどこの？"}, {"author": "x", "text": "尊い"}]
    assert hs.pick_questions(replies) == ["このニットどこの？"]


def test_within_and_ig_code_and_full_size():
    assert hs.within(NOW - datetime.timedelta(hours=29), NOW, 30) and not hs.within(NOW - datetime.timedelta(hours=31), NOW, 30)
    assert not hs.within(None, NOW, 30) and not hs.within(NOW + datetime.timedelta(hours=1), NOW, 30)
    assert hs.ig_code("/snowman.official.9/p/DABC_12-x/?img_index=1") == "DABC_12-x" and hs.ig_code("/x/reel/R1/") == "R1" and hs.ig_code("/x/") == ""
    assert hs.full_size("https://pbs.twimg.com/media/A?format=jpg&name=small").endswith("name=large")
    assert hs.full_size("https://i.ytimg.com/vi/a/hqdefault.jpg") == "https://i.ytimg.com/vi/a/hqdefault.jpg"


def test_ig_caption():
    assert hs.ig_caption('November 13, 2026、124K likes, 541 comments - snowman.official.9: "アメリカでも\nグッタイム"') == "アメリカでも\nグッタイム"
    assert hs.ig_caption('x - y: "オフショ #しょっぴー".') == "オフショ #しょっぴー"
    assert hs.ig_caption("November 5, 2026、74K likes, 416 comments - key_to_lit_official") == "" and hs.ig_caption("") == ""


def test_x_post_item_and_yt_items():
    acc = {"handle": "SN__20200122", "name": "Snow Man公式X"}
    raw = {"handle": "SN__20200122", "id": "123", "datetime": "2026-11-14T03:00:00.000Z", "text": "オフショット",
           "images": ["https://pbs.twimg.com/media/A?name=small"], "posters": [], "context": ""}
    it = hs.x_post_item(raw, "snowman", acc)
    assert it["key"] == "x:123" and it["url"] == "https://x.com/SN__20200122/status/123" and not it["repost"] and not it["video"]
    assert hs.x_post_item(dict(raw, context="Snow Manさんがリポスト", handle="other"), "snowman", acc)["repost"]
    assert hs.x_post_item(dict(raw, id=""), "snowman", acc) is None and hs.x_post_item(dict(raw, datetime=""), "snowman", acc) is None
    yt = hs.yt_items(YT, "snowman", {"name": "Snow Man公式YouTube"})
    assert yt[0]["key"] == "yt:abcdefghijk" and yt[0]["image_urls"] == ["https://i.ytimg.com/vi/abcdefghijk/hqdefault.jpg"]


def test_active_accounts_only_checked():
    sources = {"groups": {"snowman": {"youtube": [{"name": "y", "channel_id": "UC1"}, {"name": "n", "channel_id": None}],
                                      "x": [{"handle": "ok", "checked": "2026-11-14"}, {"handle": "ng", "checked": None}], "instagram": []}}}
    got = hs.active_accounts(sources)
    assert [(k, a.get("handle") or a["name"]) for _, k, a in got] == [("youtube", "y"), ("x", "ok")]
    assert len(hs.active_accounts(sources, include_unchecked=True)) == 3 and hs.active_accounts(sources, sites=["travis"]) == []


def test_html_escapes_and_text_lists_photos(tmp_path):
    it = {"key": "x:1", "group": "snowman", "platform": "x", "account": "A<b>", "handle": "h", "url": "https://x.com/h/status/1", "date": NOW,
          "text": "<script>x</script>", "images": ["img/a.jpg"], "image_urls": [], "video": False, "repost": False, "pinned": False,
          "questions": ["どこの？"], "new": True}
    html = hs.to_html([it], ["X だめ"], 30, NOW)
    assert "<script>x" not in html and "A&lt;b&gt;" in html and "どこの？" in html and "新着" in html and "集められなかったもの" in html
    assert str(tmp_path / "img/a.jpg") in hs.to_text([it], [], tmp_path, 30)


# ---------------- toolbox
def test_toolbox_commands_for_new_tools():
    cmd = toolbox.build_command("hasshin", {"site": "snowman", "hours": "48", "ytonly": "1"})
    assert cmd[2].endswith("hasshin.py") and cmd[3:] == ["--hours", "48", "--site", "snowman", "--no-browser"]
    assert toolbox.build_command("hasshin", {"hours": "abc"})[3:] == ["--hours", "30"]
    assert toolbox.build_command("rival", {"site": "", "hours": "72"})[3:] == ["--hours", "72"]
    cmd = toolbox.build_command("rival-add", {"url": "https://e.com/", "site": "travis"})
    assert cmd[3:] == ["--add", "https://e.com/", "--group", "travis"]
    for bad in ({"url": "e.com"}, {"url": "https://e.com/ --x", "site": "travis"}, {"url": "https://e.com/"}):
        try:
            toolbox.build_command("rival-add", bad)
            assert False
        except ValueError:
            pass
