# -*- coding: utf-8 -*-
"""マツの道具(blogkit / fact_check / xpost_ideas / ai_hubのollama)の純粋関数のテスト。"""
import datetime

import ai_hub
import blogkit
import fact_check as fc
import xpost_ideas as xp

TODAY = datetime.date(2026, 11, 14)
GROUPS = fc.load_groups()


# ---------------- blogkit
def test_parse_env_strips_quotes_and_comments():
    env = blogkit.parse_env('# c\nA=1\nB="x y"\n\nC=\'z\'\nbad line\n')
    assert env == {"A": "1", "B": "x y", "C": "z"}


def test_merge_env_drive_wins_except_local_first_keys():
    local = {"WP_TREND_URL": "old", "GOOGLE_INDEXING_CREDENTIALS_PATH": "/mac/key.json", "ONLY_LOCAL": "1"}
    drive = {"WP_TREND_URL": "new", "GOOGLE_INDEXING_CREDENTIALS_PATH": "C:\\win\\key.json", "WP_CHOMO2_URL": "u", "EMPTY": ""}
    out = blogkit.merge_env(local, drive)
    assert out["WP_TREND_URL"] == "new" and out["WP_CHOMO2_URL"] == "u" and out["ONLY_LOCAL"] == "1"
    assert out["GOOGLE_INDEXING_CREDENTIALS_PATH"] == "/mac/key.json"
    assert "EMPTY" not in out
    assert blogkit.merge_env({}, drive)["GOOGLE_INDEXING_CREDENTIALS_PATH"] == "C:\\win\\key.json"


def test_author_for_matches_hostname_prefix():
    assert blogkit.author_for("trend", "Tomoki-GEEKOM") == 4
    assert blogkit.author_for("trend", "USER1") == 3
    assert blogkit.author_for("snowman", "Yuka-MacBook-NEO.local") == 1
    assert blogkit.author_for("trend", "Yuka-MacBook-NEO") is None


def test_site_by_url_and_strip_mi():
    assert blogkit.site_by_url("https://chomoand-4.blog/abc-123/") == "travis"
    assert blogkit.site_by_url("https://example.com/") is None
    assert blogkit.strip_mi("【未】【すとらじ】私服はどこの？") == "【すとらじ】私服はどこの？"


def test_blocks_are_gutenberg_blocks():
    b = blogkit.Blocks()
    assert b.p("a。", "b。") == "<!-- wp:paragraph -->\n<p>a。<br>\nb。</p>\n<!-- /wp:paragraph -->\n\n"
    assert '<h3 class="wp-block-heading">x</h3>' in b.h3("x") and '{"level":3}' in b.h3("x")
    t = b.table(("a", "b"), [("1", "2"), ("3", "4")])
    assert t.count("<tr>") == 3 and "wp:table" in t and b.A in t
    assert "この記事でわかること" in b.wakaru(["x"]) and "&#10003;" in b.checks(["x"])
    assert "q=%E6%B5%9C%E6%9D%BE" in b.gmap("浜松")


# ---------------- fact_check: 日付
def test_dates_ok_and_wrong_weekday():
    assert fc.check_dates("2026年11月18日(水)よる10時から", TODAY) == ([], [])
    ng, _ = fc.check_dates("2026年11月18日(木)に配信", TODAY)
    assert len(ng) == 1 and "(水)" in ng[0]
    assert fc.check_dates("11/18(水)と11月18日(水曜)", TODAY) == ([], [])


def test_dates_fullwidth_and_holiday_and_invalid():
    assert fc.check_dates("11月23日（月・祝）", TODAY) == ([], [])
    ng, _ = fc.check_dates("2月30日(月)", TODAY)
    assert "存在しない" in ng[0]


def test_dates_without_year_uses_nearby_year_or_warns():
    # 2027年1月1日は金曜。直前に2027年と書いてあればそれを使う
    assert fc.check_dates("2027年のお正月。1月1日(金)に放送", TODAY) == ([], [])
    ng, warn = fc.check_dates("1月1日(金)に放送", TODAY)  # 今年(2026)なら木曜、来年なら合う
    assert ng == [] and len(warn) == 1 and "2027" in warn[0]


# ---------------- fact_check: 名前
def test_variants_make_common_typos():
    assert fc.variants("髙地優吾") == ["高地優吾"]
    assert "岩崎大昇" in fc.variants("岩﨑大昇")
    assert fc.variants("目黒蓮") == []


def test_wrong_map_never_contains_a_correct_name():
    wm = fc.wrong_map(GROUPS)
    correct = [m["name"] for m in fc.all_members(GROUPS)] + [c["label"] for c in GROUPS.values()]
    for w in wm:
        assert not any(w in c for c in correct), w
    assert wm["高地優吾"] == "髙地優吾" and wm["宮館涼太"] == "宮舘涼太" and wm["SnowMan"] == "Snow Man"
    assert wm["宮館亮太"] == "宮舘涼太"  # まちがい+旧字の合わせ技


def test_check_names_flags_typos_only():
    assert fc.check_names("髙地優吾さんと岩﨑大昇さん、Snow Manの目黒蓮さん", GROUPS) == []
    ng = fc.check_names("高地優吾さんと渡邊翔太さん", GROUPS)
    assert len(ng) == 2 and any("髙地優吾" in x for x in ng)


# ---------------- fact_check: 年齢・誕生日・カラー
def test_profiles_age_and_birthday():
    # 松倉海斗 1997-11-14生まれ → 2026-11-14で29歳
    assert fc.check_profiles("松倉海斗さん(29)は元気です。", GROUPS, TODAY) == ([], [])
    ng, _ = fc.check_profiles("松倉海斗さんは現在27歳です。", GROUPS, TODAY)
    assert len(ng) == 1 and "29歳" in ng[0]
    ng, _ = fc.check_profiles("松倉海斗さんは11月15日生まれです。", GROUPS, TODAY)
    assert len(ng) == 1 and "11月14日" in ng[0]
    assert fc.check_profiles("松倉海斗さんの誕生日は11月14日です。", GROUPS, TODAY) == ([], [])


def test_profiles_color_only_when_one_member_in_sentence():
    _, warn = fc.check_profiles("目黒蓮さんのメンバーカラーは赤です。", GROUPS, TODAY)
    assert len(warn) == 1 and "黒" in warn[0]
    assert fc.check_profiles("目黒蓮さんのメンバーカラーは黒です。", GROUPS, TODAY) == ([], [])
    assert fc.check_profiles("目黒蓮さんは黒、宮舘涼太さんのメンカラは赤です。", GROUPS, TODAY) == ([], [])


# ---------------- fact_check: タイトル・形・言葉・リンク
def test_title_rules():
    assert fc.check_title("知念侑李の免許合宿はどこ？", "本文") == ([], [])
    ng, warn = fc.check_title("あ" * 36, "本文")
    assert any("36字" in x for x in ng) and any("終わっていない" in x for x in warn)
    ng, _ = fc.check_title("どこ?", "本文")
    assert any("半角" in x for x in ng)
    _, warn = fc.check_title("5選はこれ！", "全部で4つ紹介します")
    assert any("「5」" in x for x in warn)
    assert fc.check_title("【未】第5話の犯人は誰？", "第5話のあらすじ") == ([], [])


def test_shape_rules():
    good = "<!-- wp:heading --><h2>a</h2><!-- /wp:heading --><!-- wp:paragraph --><p>" + "あ" * 2600 + "</p>"
    assert fc.check_shape(good) == ([], [])
    ng, _ = fc.check_shape("<h2>a</h2><p>短い</p><hr>")
    assert len(ng) == 3  # 字数・ブロック形式・区切り線
    _, warn = fc.check_shape(good + "<p>一。二。三。四。</p>")
    assert any("<br>" in x for x in warn)


def test_sensitive_words_need_soft_wording():
    assert fc.check_sensitive("A高校に通っていると推測されます。") == []
    assert len(fc.check_sensitive("A高校に通っています。")) == 1


def test_urls_extract_and_classify():
    html = ('<a href="https://x.com/a/status/123?s=20">x</a><img src="https://e.com/a.jpg">'
            '<div class="wp-block-embed__wrapper">\nhttps://youtu.be/abcdefghijk\n</div>')
    urls = fc.extract_urls(html)
    assert [fc.classify_url(u) for u in urls] == ["x", "web", "youtube"]
    assert fc.classify_url("https://www.amazon.co.jp/dp/x") == "skip"


def test_plain_and_char_count():
    assert fc.plain("<p>a<br>b</p><!-- c --><script>x</script>") == "a\nb"
    assert fc.char_count("<p>あ い\nう</p>") == 3


# ---------------- xpost_ideas
GOOD = "Snow Manの目黒蓮くんが着てたニットが破壊力えぐい😭🔥\nお値段なんと95,700円…！"


def test_xpost_good_passes():
    assert xp.problems(GOOD, "#SnowMan #目黒蓮") == []


def test_xpost_rejects_rule_breakers():
    tags = "#SnowMan #目黒蓮"
    assert any("誘導" in x for x in xp.problems(GOOD + "\n詳細はコメント欄に👇", tags))
    assert any("URL" in x for x in xp.problems(GOOD + " https://a.com/x", tags))
    assert any("答え" in x for x in xp.problems(GOOD + "セリーヌ！", tags, hide=["セリーヌ"]))
    assert any("ハッシュタグ" in x for x in xp.problems(GOOD, "#SnowMan"))
    assert any("固有名詞" in x for x in xp.problems("あのニットが可愛すぎる😭", "#a1 #b2"))
    assert any("長い" in x for x in xp.problems("目黒蓮" + "あ" * 130, tags))
    assert xp.problems("目黒蓮くんと向井康二くんのリンクコーデ優勝🏆", tags) == []  # 「リンクコーデ」は誘導ではない


def test_xpost_parse_candidates():
    ai = "案1: え、目黒蓮くん…😭\n値段がやばい\n#SnowMan #目黒蓮\n---\n2. 速報🚨\n＃SnowMan #すの担\n"
    assert xp.parse_candidates(ai) == [("え、目黒蓮くん…😭\n値段がやばい", "#SnowMan #目黒蓮"), ("速報🚨", "#SnowMan #すの担")]


def test_xpost_notes_and_prompt():
    assert xp.notes("待って、無理") and not xp.notes("え、無理")
    p = xp.build_prompt("本文", "題", "trend", 3, ["セリーヌ"])
    assert "セリーヌ" in p and "くん付けもしない" in p and "3案" in p


# ---------------- ai_hub: ollama
def test_pick_ollama_model():
    assert ai_hub.pick_ollama_model([], "gemma3") is None
    assert ai_hub.pick_ollama_model(["gemma3:12b", "x:1"], None) == "gemma3:12b"
    assert ai_hub.pick_ollama_model(["a:1", "gemma3:4b"], "gemma3") == "gemma3:4b"
    assert ai_hub.pick_ollama_model(["a:1"], "missing") == "a:1"
