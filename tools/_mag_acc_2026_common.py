# -*- coding: utf-8 -*-
"""雑誌着用アクセまとめ2026(SM/ST/TJ)の3本で共有する画像まわり(2026-11-21)。

画像は images/mag_acc_2026/<グループ>_<ツイートID>_<n>.jpg(ブランド公式の告知ポストの商品写真)。
WordPressに上げたIDとURLは articles/<KEY>_media.json に控え、2回目からは上げ直さない。
"""
import json

import blogkit

IMG_DIR = blogkit.ROOT / "images" / "mag_acc_2026"


class Media(object):
    def __init__(self, site, key, b):
        self.site, self.b = site, b
        self.path = blogkit.ARTICLES / (key + "_media.json")
        self.m = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {}
        self.wp = None

    def ensure(self, items):
        """items = {ファイル名(拡張子なし): alt}。未アップの分だけ上げる。"""
        for k, alt in items.items():
            if k in self.m:
                continue
            self.wp = self.wp or blogkit.WP(self.site)
            mid = self.wp.upload_media(str(IMG_DIR / (k + ".jpg")), alt)
            src = self.wp.get("/media/{}".format(mid))["source_url"]
            self.m[k] = {"id": mid, "url": src, "alt": alt}
            self.path.write_text(json.dumps(self.m, ensure_ascii=False, indent=1), encoding="utf-8")
            print("画像を上げた:", k, mid)

    def fig(self, k, user, w=360):
        """k=ファイル名。user=出典のXアカウント名(@なし)。ツイートIDはファイル名から取る。"""
        tid = k.split("_")[1]
        if k in self.m:
            url, alt = self.m[k]["url"], self.m[k]["alt"]
        else:  # --build-only のとき(まだ上げていない)
            url, alt = "https://example.invalid/" + k + ".jpg", k
        src = "https://x.com/{}/status/{}".format(user, tid)
        return self.b.html(
            '<figure class="wp-block-image size-large"><img src="{0}" alt="{1}" '
            'style="max-width:{3}px;width:100%;height:auto;display:block;margin:0 auto;">'
            '<figcaption style="font-size:0.8em;color:#888;text-align:center;">出典：'
            '<a href="{2}" target="_blank" rel="noopener">{2}</a></figcaption></figure>'.format(url, alt, src, w))


# ---- アフィリエイト(楽天APIはこのPCのIPが未許可なので、楽天の検索結果ページへのアフィリエイトリンク+Amazon検索)
import urllib.parse  # noqa: E402

import affiliate_box as ab  # noqa: E402
import affiliate_linker as al  # noqa: E402

_ENV = ab.load_keys()
NOTICE = ab.NOTICE + "\n\n"


def rk_url(q):
    t = urllib.parse.quote("https://search.rakuten.co.jp/search/mall/" + urllib.parse.quote(q) + "/", safe="")
    return "https://hb.afl.rakuten.co.jp/hgc/{}/?pc={}&m={}".format(_ENV["RAKUTEN_AFFILIATE_ID"], t, t)


def aff(title, q, border, note=""):
    """楽天/Amazonの検索ボタン枠。q=検索ワード(ブランド名+アイテム)。"""
    return ab.build_box(rk_url(q), None, title, al.build_amazon_search_url(q, _ENV.get("AMAZON_ASSOCIATE_TAG")),
                        note=note, border=border) + "\n\n"
