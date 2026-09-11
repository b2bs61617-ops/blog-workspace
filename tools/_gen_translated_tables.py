# -*- coding: utf-8 -*-
"""Extract the utawari lyric table from each JP .md article and produce KR/EN
versions by replacing ONLY the header/section labels (anchored by '>' and
'</th>' or '</td>' so lyric/member text can never be accidentally matched).
Member names, colors and lyric lines are left byte-for-byte identical."""
import re

REPO = r"C:\Users\s30se\Desktop\blog-workspace"

HEADER_MAP = {
    "kr": {"\u5c55\u958b": "\uad6c\uac04", "\u6b4c\u3046\u30e1\u30f3\u30d0\u30fc": "\ubd80\ub974\ub294 \uba64\ubc84", "\u6b4c\u8a5e": "\uac00\uc0ac"},
    "en": {"\u5c55\u958b": "Section", "\u6b4c\u3046\u30e1\u30f3\u30d0\u30fc": "Member(s)", "\u6b4c\u8a5e": "Lyrics"},
}

RA_SECTION_MAP = {
    "kr": {
        "1\u756a Aメロ": "1\uc808 A\uba5c\ub85c\ub514", "1\u756a Bメロ": "1\uc808 B\uba5c\ub85c\ub514",
        "1\u756a \u30d7\u30ea\u30b3\u30fc\u30e9\u30b9": "1\uc808 \ud504\ub9ac\ucf54\ub7ec\uc2a4", "\u30b5\u30d3\u524d": "\uc0ac\ube44 \uc9c1\uc804",
        "1\u756a \u30b5\u30d3": "1\uc808 \uc0ac\ube44", "2\u756a Aメロ": "2\uc808 A\uba5c\ub85c\ub514", "2\u756a Bメロ": "2\uc808 B\uba5c\ub85c\ub514",
        "2\u756a \u30d7\u30ea\u30b3\u30fc\u30e9\u30b9": "2\uc808 \ud504\ub9ac\ucf54\ub7ec\uc2a4", "\u30d6\u30ea\u30c3\u30b8": "\ube0c\ub9bf\uc9c0", "\u30e9\u30c3\u30d7": "\ub7a9",
        "\u5927\u30b5\u30d3\u524d": "\ub77c\uc2a4\ud2b8 \uc0ac\ube44 \uc9c1\uc804", "\u5927\u30b5\u30d3": "\ub77c\uc2a4\ud2b8 \uc0ac\ube44", "\u30a2\u30a6\u30c8\u30ed": "\uc544\uc6c3\ud2b8\ub85c",
    },
    "en": {
        "1\u756a Aメロ": "Verse 1 (A-melody)", "1\u756a Bメロ": "Verse 1 (B-melody)",
        "1\u756a \u30d7\u30ea\u30b3\u30fc\u30e9\u30b9": "Pre-Chorus 1", "\u30b5\u30d3\u524d": "Chorus Lead-in",
        "1\u756a \u30b5\u30d3": "Chorus 1", "2\u756a Aメロ": "Verse 2 (A-melody)", "2\u756a Bメロ": "Verse 2 (B-melody)",
        "2\u756a \u30d7\u30ea\u30b3\u30fc\u30e9\u30b9": "Pre-Chorus 2", "\u30d6\u30ea\u30c3\u30b8": "Bridge", "\u30e9\u30c3\u30d7": "Rap",
        "\u5927\u30b5\u30d3\u524d": "Final Chorus Lead-in", "\u5927\u30b5\u30d3": "Final Chorus", "\u30a2\u30a6\u30c8\u30ed": "Outro",
    },
}

BA_SECTION_MAP = {
    "kr": {
        "1\u756a Aメロ": "1\uc808 A\uba5c\ub85c\ub514", "1\u756a Bメロ": "1\uc808 B\uba5c\ub85c\ub514",
        "1\u756a \u30d7\u30ea\u30b3\u30fc\u30e9\u30b9": "1\uc808 \ud504\ub9ac\ucf54\ub7ec\uc2a4", "\u9593\u594f(Pray)": "\uac04\uc8fc(Pray)",
        "1\u756a \u30b5\u30d3": "1\uc808 \uc0ac\ube44", "2\u756a Aメロ": "2\uc808 A\uba5c\ub85c\ub514", "2\u756a Bメロ": "2\uc808 B\uba5c\ub85c\ub514",
        "\u9593\u594f": "\uac04\uc8fc", "2\u756a \u30d7\u30ea\u30b3\u30fc\u30e9\u30b9": "2\uc808 \ud504\ub9ac\ucf54\ub7ec\uc2a4", "\u30d6\u30ea\u30c3\u30b8": "\ube0c\ub9bf\uc9c0",
        "\u5927\u30b5\u30d3": "\ub77c\uc2a4\ud2b8 \uc0ac\ube44",
    },
    "en": {
        "1\u756a Aメロ": "Verse 1 (A-melody)", "1\u756a Bメロ": "Verse 1 (B-melody)",
        "1\u756a \u30d7\u30ea\u30b3\u30fc\u30e9\u30b9": "Pre-Chorus 1", "\u9593\u594f(Pray)": "Interlude (\u201cPray\u201d)",
        "1\u756a \u30b5\u30d3": "Chorus 1", "2\u756a Aメロ": "Verse 2 (A-melody)", "2\u756a Bメロ": "Verse 2 (B-melody)",
        "\u9593\u594f": "Interlude", "2\u756a \u30d7\u30ea\u30b3\u30fc\u30e9\u30b9": "Pre-Chorus 2", "\u30d6\u30ea\u30c3\u30b8": "Bridge",
        "\u5927\u30b5\u30d3": "Final Chorus",
    },
}


def extract_table(md_text):
    start = md_text.index('<div style="overflow-x:auto;">')
    start = md_text.rindex("<!-- wp:html -->", 0, start)
    end = md_text.index("<!-- /wp:html -->", start) + len("<!-- /wp:html -->")
    return md_text[start:end]


def translate_table(html, header_map, section_map):
    out = html
    for ja, tr in header_map.items():
        out = out.replace(f">{ja}</th>", f">{tr}</th>")
    for ja, tr in section_map.items():
        out = out.replace(f">{ja}</td>", f">{tr}</td>")
    return out


for key, section_maps in [("run_again", RA_SECTION_MAP), ("black_angel", BA_SECTION_MAP)]:
    md = open(f"{REPO}\\articles\\ko1keyz_{key}_utawari.md", encoding="utf-8").read()
    table_ja = extract_table(md)
    for lang in ("kr", "en"):
        table_tr = translate_table(table_ja, HEADER_MAP[lang], section_maps[lang])
        # sanity: label substitution should have changed nothing about row/member counts
        assert table_tr.count("<tr>") == table_ja.count("<tr>"), f"{key}/{lang} row count mismatch"
        assert table_tr.count("<td") == table_ja.count("<td"), f"{key}/{lang} td count mismatch"
        out_path = f"{REPO}\\tools\\_gen_table_{key}_{lang}.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(table_tr)
        print(f"wrote {out_path} ({len(table_tr)} chars)")
        # report any JA labels that failed to translate (still contain untranslated bold nowrap cells with kanji)
        leftover = re.findall(r'white-space:nowrap;vertical-align:top;">([^<]+)</td>', table_tr)
        untranslated = [l for l in leftover if any('\u3040' <= ch <= '\u30ff' or '\u4e00' <= ch <= '\u9fff' for ch in l)]
        if untranslated:
            print(f"  !! possibly untranslated section labels remain: {untranslated}")
