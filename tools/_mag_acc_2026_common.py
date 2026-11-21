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
