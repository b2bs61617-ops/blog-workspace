# -*- coding: utf-8 -*-
"""Shared helpers for TV schedule articles 11/15-11/21 (5 groups)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _build_tv_schedule_1108_1114 as _b
from _build_tv_schedule_1108_1114 import p, h2, h3, html, PASTEL, mc, save  # noqa: F401

NOTE_LINES = ["※2026年11月12日時点の情報で、11/19(木)分までは番組表をもとにしています。",
              "11/20(金)・21(土)分は番組表がまだ出ていないため、毎週の放送枠や公式の告知から(予定)として載せました。",
              "放送内容や時間は変わる場合があるので、最新情報は公式サイトや番組表でご確認ください。"]
NOTE_P = p(*NOTE_LINES)


class Theme(_b.Theme):
    def summary(self, items):
        chk = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {self.main};border-radius:3px;'
               f'color:{self.main};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')
        ps = "\n".join(f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};">{chk}{t}</p>' for i, t in enumerate(items))
        return html(f'<div style="border:1px solid {self.main};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{self.light};">\n'
                    f'{ps}\n</div>')
