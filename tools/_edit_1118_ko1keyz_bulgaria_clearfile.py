# -*- coding: utf-8 -*-
"""KO1KEYZ ブルガリア クリアファイル記事 JP15907/KR15910/EN15911 を11/18 18:30版でリライト(WP本文へ直接パッチ・1回きり)。

- @namonaki_suika まとめ(11/18 18:30): 東京(町田)の相鉄ローゼンでも発見、群馬とりせんは残りわずか
- 相鉄ローゼンは人気で「ファイル残り10枚ほど」「ファイルはあるが商品が品切れ→再入荷で再開(発注は最速で明後日)」
- 会計後にサービスカウンターでレシートを見せてもらうお店もある(売り場の貼り紙写真)
- 埼玉(イオン・ヨークマート・タイラヤ・アルプス)・三重(一号舘)・鹿児島(ニシムタ)はなし
- 他のスーパーは明治×ディズニー小皿キャンペーン中が多く、終わってから切り替わるかも
    python tools/_edit_1118_ko1keyz_bulgaria_clearfile.py                       # 確認だけ
    python tools/_edit_1118_ko1keyz_bulgaria_clearfile.py --apply --pop 画像   # 画像アップ+更新
"""
import io
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import blogkit  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 11/17版の目撃表を読み込んで差分だけ直す
_src = (HERE / "_edit_1117_ko1keyz_bulgaria_clearfile.py").read_text(encoding="utf-8")
_ns = {}
exec(_src[_src.index("# ------------------------------------------------------------------ 目撃表"):
          _src.index("# ------------------------------------------------------------------ 言語ごとの中身")], _ns)

b = blogkit.Blocks("#c2410c", "#f2c9a8", "#fff7ef")
w = blogkit.WP("ko1keyz")
APPLY = "--apply" in sys.argv
SRC = "https://x.com/namonaki_suika/status/2122975214699225350"
POP_FILE = sys.argv[sys.argv.index("--pop") + 1] if "--pop" in sys.argv else None


def upd(rows, key, found=None, notfound=None):
    for i, r in enumerate(rows):
        if r[0] == key:
            rows[i] = (r[0], found or r[1], notfound or r[2])
            return
    raise SystemExit("row not found: " + key)


def ins(rows, after, row):
    i = [r[0] for r in rows].index(after)
    rows.insert(i + 1, row)


JP_ROWS = list(_ns["JP_ROWS"])
upd(JP_ROWS, "群馬・北関東", found="とりせん(群馬・残りわずかのお店も)")
upd(JP_ROWS, "埼玉", notfound="ベルク・BIGA・東武ストア・ヤオコー・コモディイイダ・イオン・ヨークマート・タイラヤ・アルプス")
upd(JP_ROWS, "東京", found="相鉄ローゼン(町田市)")
upd(JP_ROWS, "神奈川", notfound="相鉄ローゼン(置いていないお店・商品が品切れのお店も)")
upd(JP_ROWS, "鹿児島", notfound="タイヨー・Aコープ・ニシムタ")
ins(JP_ROWS, "愛知", ("三重", "ー", "一号舘"))

KR_ROWS = list(_ns["KR_ROWS"])
upd(KR_ROWS, "군마・기타칸토", found="토리센(군마・거의 남지 않은 매장도)")
upd(KR_ROWS, "사이타마", notfound="베르크・BIGA・도부스토어・야오코・코모디이이다・이온・요크마트・다이라야・알프스")
upd(KR_ROWS, "도쿄", found="소테쓰 로젠(마치다시)")
upd(KR_ROWS, "가나가와", notfound="소테쓰 로젠(없는 매장・상품 품절 매장도)")
upd(KR_ROWS, "가고시마", notfound="타이요・A코프・니시무타")
ins(KR_ROWS, "아이치", ("미에", "ー", "이치고칸"))

EN_ROWS = list(_ns["EN_ROWS"])
upd(EN_ROWS, "Gunma / North Kanto", found="Torisen (Gunma; almost gone at some stores)")
upd(EN_ROWS, "Saitama", notfound="Belc, BIGA, Tobu Store, Yaoko, Commodi Iida, AEON, York Mart, Tairaya, Alps")
upd(EN_ROWS, "Tokyo", found="Sotetsu Rosen (Machida)")
upd(EN_ROWS, "Kanagawa", notfound="Sotetsu Rosen (not every store; some out of the drinks)")
upd(EN_ROWS, "Kagoshima", notfound="Taiyo, A-Coop, Nishimuta")
ins(EN_ROWS, "Aichi", ("Mie", "–", "Ichigokan"))


def fig(url, alt, cap):
    return b.html('<figure class="wp-block-image size-large">\n'
                  '  <img src="{}" alt="{}" style="max-width:100%;height:auto;">\n'
                  '  <figcaption>{}{}</figcaption>\n</figure>'.format(url, alt, cap, SRC))


# ------------------------------------------------------------------ JP
def jp_counter(img):
    s = b.p("ただし、もらい方はお店によってちがうこともあります。",
            "11月18日には、売り場に「" + b.mark("クリアファイルご希望のお客様は会計後サービスカウンターにてレシート確認の上お渡しいたします") + "」という貼り紙があるお店も見つかりました。")
    s += img
    s += b.p("売り場にファイルが見当たらないときは、レシートを持ってサービスカウンターで聞いてみましょう。")
    return s


def jp_sight():
    s = b.h3("全国の目撃情報(11月18日18時半時点)")
    s += b.p("18日の18時半時点では、" + b.mark("「あった」は相鉄ローゼン(神奈川・東京の町田市)と群馬のとりせん") + "です。",
             "東京でも、町田市にある相鉄ローゼンで見つかりました。ほかの地域は、まだ「なかった」という声ばかりです。")
    s += b.table(("地域", "あった", "なかった"), JP_ROWS)
    s += b.p("※同じチェーンでも、お店によってある・なしがちがいます。回ったお店の一部だけの声です。",
             "※中国地方・高知・徳島・香川・熊本などは、まだ情報がありません。")
    s += b.h3("人気で品切れのお店も")
    s += b.p("相鉄ローゼンでは、サービスカウンターで「" + b.mark("なんだかすごく人気みたいですね") + "」と言われたという声がありました。",
             "そのお店では、ファイルは残り10枚ほど。対象の商品がなくなっても、また入荷すれば配るのを再開できそうとのことです。")
    s += b.p("ほかにも、" + b.mark("ファイルはあるのに、ブルガリアの商品のほうが売り切れ") + "という相鉄ローゼンがありました。",
             "お店の人の話では、発注しても最速で明後日。入荷までは少し時間がかかりそうです。")
    s += b.p("群馬のとりせんでは「6箱分の飲み物のうち5箱が売れた」ほど人気で、残り3枚だったお店もあったそうです。",
             "同じ相鉄ローゼンでも、ONE SHOTそのものを置いていないお店もありました。")
    s += b.p("POPだけで売り場にファイルがないときは、店員さんに聞いてみましょう。神奈川県西部では、言うと持ってきてくれたお店もあったそうです。",
             "上のほうにかけてあって見落とした、という声もあるので、" + b.mark("ヨーグルトの棚の上のほうまで") + "よく見てみてくださいね。")
    s += b.p("いっぽう、ほかのスーパーでは、今は明治の" + b.mark("ディズニーの小皿がもらえるキャンペーン") + "をしているお店が多いそうです。",
             "兵庫でも「ディズニーのパッケージが終わったあとに始める」と言われたお店がありました。ディズニーのキャンペーンが終わったあとに、クリアファイルに切り替わるお店もありそうです。")
    s += b.p("遠くまで探しに行く前に、近くのお店を数日あけてもう一度のぞいてみるのもおすすめです。")
    return s


JP_SUM = ["KO1KEYZ×ONE SHOTのオリジナルクリアファイルが、一部のお店で配られている",
          "条件は対象商品(ONE SHOTシリーズ全品)を2本買うこと。売り場のPOPにも書いてある",
          "会計後にサービスカウンターでレシートを見せてもらうお店もある",
          "お店の施策なので、公式からの案内やお店の一覧は出ない見込み",
          "11月18日時点で見つかったのは、相鉄ローゼン(神奈川・東京の町田市)・とりせん(群馬)",
          "人気で商品やファイルが品切れのお店も。再入荷やディズニーのキャンペーン終了後に始まるお店に期待"]

# ------------------------------------------------------------------ KR
def kr_counter(img):
    s = b.p("다만 받는 방법은 매장마다 다를 수도 있습니다.",
            "11월 18일에는 매장에 '" + b.mark("클리어 파일을 원하시는 고객님은 계산 후 서비스 카운터에서 영수증 확인 후 드립니다") + "'라는 안내문이 붙은 곳도 발견됐습니다.")
    s += img
    s += b.p("매대에 파일이 안 보이면 영수증을 들고 서비스 카운터에 물어보세요.")
    return s


def kr_sight():
    s = b.h3("전국 목격 정보(11월 18일 18시 반 기준)")
    s += b.p("18일 18시 반 기준으로 " + b.mark("'있었다'는 소테쓰 로젠(가나가와・도쿄 마치다시)과 군마의 토리센") + "입니다.",
             "도쿄에서도 마치다시의 소테쓰 로젠에서 발견됐습니다. 다른 지역은 아직 '없었다'는 목소리뿐입니다.")
    s += b.table(("지역", "있었다", "없었다"), KR_ROWS)
    s += b.p("※같은 체인이라도 매장마다 다릅니다. 돌아본 일부 매장의 목소리입니다.",
             "※주고쿠 지방・고치・도쿠시마・가가와・구마모토 등은 아직 정보가 없습니다.")
    s += b.h3("인기 때문에 품절된 매장도")
    s += b.p("소테쓰 로젠에서는 서비스 카운터에서 '" + b.mark("왠지 엄청 인기가 많은 것 같네요") + "'라는 말을 들었다는 목소리가 있었습니다.",
             "그 매장은 파일이 10장 정도 남았고, 대상 상품이 다 팔려도 다시 입고되면 배포를 재개할 수 있을 것 같다고 합니다.")
    s += b.p("또 " + b.mark("파일은 있는데 불가리아 상품이 품절") + "된 소테쓰 로젠도 있었습니다.",
             "매장 직원 말로는 발주해도 빨라야 모레. 입고까지는 시간이 좀 걸릴 것 같습니다.")
    s += b.p("군마의 토리센에서는 '음료 6박스 중 5박스가 팔렸다'고 할 만큼 인기여서, 3장만 남은 매장도 있었다고 합니다.",
             "같은 소테쓰 로젠이라도 ONE SHOT 자체를 두지 않은 매장도 있었습니다.")
    s += b.p("POP만 있고 매대에 파일이 없으면 점원에게 물어보세요. 가나가와현 서부에서는 말하니 가져다준 매장도 있었다고 합니다.",
             "위쪽에 걸려 있어서 못 봤다는 목소리도 있으니 " + b.mark("요구르트 진열대 위쪽까지") + " 꼼꼼히 확인해 보세요.")
    s += b.p("한편 다른 슈퍼에서는 지금 메이지의 " + b.mark("디즈니 작은 접시를 받는 캠페인") + "을 하는 곳이 많다고 합니다.",
             "효고에서도 '디즈니 패키지가 끝난 뒤에 시작한다'는 매장이 있었습니다. 디즈니 캠페인이 끝난 뒤 클리어 파일로 바뀌는 매장도 있을 것 같습니다.")
    s += b.p("멀리까지 찾으러 가기 전에, 가까운 매장을 며칠 뒤 다시 들러 보는 것도 추천합니다.")
    return s


KR_SUM = ["KO1KEYZ×ONE SHOT 오리지널 클리어 파일이 일본 일부 매장에서 배포 중",
          "조건은 대상 상품(ONE SHOT 시리즈 전 제품) 2개 구매. 매장 POP에도 적혀 있음",
          "계산 후 서비스 카운터에서 영수증을 확인하고 주는 매장도 있음",
          "매장별 행사라서 공식 안내나 매장 목록은 없을 전망",
          "11월 18일 기준 발견된 곳은 소테쓰 로젠(가나가와・도쿄 마치다시)・토리센(군마)",
          "인기 때문에 상품・파일이 품절된 매장도. 재입고나 디즈니 캠페인 종료 후 시작하는 매장에 기대"]

# ------------------------------------------------------------------ EN
def en_counter(img):
    s = b.p("The way you receive it can differ by store, though.",
            "On November 18, one store was found with a notice saying: \"" + b.mark("If you would like a clear file, please go to the service counter after paying; we will hand it over after checking your receipt.") + "\"")
    s += img
    s += b.p("If you cannot see any files on the shelf, take your receipt to the service counter and ask.")
    return s


def en_sight():
    s = b.h3("Sightings around Japan (as of 6:30 p.m., Nov 18)")
    s += b.p("As of 6:30 p.m. on the 18th, " + b.mark("it has been found at Sotetsu Rosen (Kanagawa and Machida, Tokyo) and Torisen in Gunma") + ".",
             "Tokyo now has a sighting too, at a Sotetsu Rosen in Machida. Every other area still has only \"not found\" reports.")
    s += b.table(("Area", "Found", "Not found"), EN_ROWS)
    s += b.p("*Results differ by store, even within one chain. These are only the stores fans checked.",
             "*No reports yet from Chugoku, Kochi, Tokushima, Kagawa, Kumamoto and some other areas.")
    s += b.h3("So popular that some stores ran out")
    s += b.p("At one Sotetsu Rosen, staff at the service counter said, \"" + b.mark("It seems to be really popular") + ".\"",
             "That store had about 10 files left, and said it could restart once the eligible drinks were restocked.")
    s += b.p("Another Sotetsu Rosen " + b.mark("still had files but had sold out of the Bulgaria drinks") + ".",
             "Staff said the earliest they could get an order in was two days later, so restocking may take a while.")
    s += b.p("At Torisen in Gunma, five of six boxes of the drinks had sold, and one store was down to its last three files.",
             "Some Sotetsu Rosen stores do not carry ONE SHOT at all.")
    s += b.p("If you see the POP but no files, ask a staff member. In western Kanagawa, staff brought one out when asked.",
             "Some fans missed it because it was hanging up high, so check " + b.mark("all the way up the yogurt shelf") + ".")
    s += b.p("Meanwhile, many other supermarkets are currently running Meiji's " + b.mark("Disney small-plate giveaway") + ".",
             "A store in Hyogo also said it would start after the Disney packaging ends. Some stores may switch to the clear file once the Disney campaign is over.")
    s += b.p("Before traveling far, it is worth checking your local stores again in a few days.")
    return s


EN_SUM = ["An original KO1KEYZ × ONE SHOT clear file is being given out at some stores in Japan",
          "Buy two eligible products (any ONE SHOT item); the in-store POP confirms it",
          "Some stores hand it out at the service counter after checking your receipt",
          "Stores run it themselves, so no official notice or store list is expected",
          "As of Nov 18, it has been found at Sotetsu Rosen (Kanagawa, Machida in Tokyo) and Torisen (Gunma)",
          "Some stores have run out of drinks or files; watch for restocks and stores starting after the Disney campaign"]

CFG = {
    15907: dict(counter=jp_counter, sight=jp_sight, summ=JP_SUM, summary="まとめ",
                h_sight="全国の目撃情報(", h_next="狙い目は大きめのスーパー",
                anchor="台紙には「商品と一緒にレジにお持ちください」と書いてあります。</p>\n<!-- /wp:paragraph -->\n\n",
                alt="クリアファイルは会計後サービスカウンターで渡すという売り場の貼り紙", cap="出典:",
                reps=[("※2026年11月17日時点の情報です。", "※2026年11月18日時点の情報です。"),
                      ("<li>全国の目撃情報(11月17日時点)</li>", "<li>全国の目撃情報(11月18日時点)</li>"),
                      ("クリアファイルを商品といっしょにレジへ持っていく",
                       "クリアファイルを商品といっしょにレジへ持っていく(会計後にサービスカウンターで渡すお店も)"),
                      ("とはいえ、17日の時点でもイオンでは", "とはいえ、18日の時点でもイオンでは"),
                      ("売り場でクリアファイルを見つけたら、2本といっしょにレジへ持っていけばよさそうです。",
                       "売り場でクリアファイルを見つけたら、2本といっしょにレジへ持っていけばよさそうです。売り場にないお店では、会計後にサービスカウンターでレシートを見せるともらえることもあります。")],
                key="11月18日18時半時点"),
    15910: dict(counter=kr_counter, sight=kr_sight, summ=KR_SUM, summary="정리",
                h_sight="전국 목격 정보(", h_next="노려볼 만한 곳은 큰 슈퍼",
                anchor="대지에는 '상품과 함께 계산대로 가져와 주세요'라고 적혀 있습니다.</p>\n<!-- /wp:paragraph -->\n\n",
                alt="클리어 파일은 계산 후 서비스 카운터에서 준다는 매장 안내문", cap="출처:",
                reps=[("※2026년 11월 17일 기준 정보입니다.", "※2026년 11월 18일 기준 정보입니다."),
                      ("<li>전국 목격 정보(11월 17일 기준)</li>", "<li>전국 목격 정보(11월 18일 기준)</li>"),
                      ("클리어 파일을 상품과 함께 계산대로 가져가기",
                       "클리어 파일을 상품과 함께 계산대로 가져가기(계산 후 서비스 카운터에서 주는 매장도)"),
                      ("다만 17일 시점에도 이온에서는", "다만 18일 시점에도 이온에서는")],
                key="11월 18일 18시 반 기준"),
    15911: dict(counter=en_counter, sight=en_sight, summ=EN_SUM, summary="Summary",
                h_sight="Sightings around Japan (", h_next="Big supermarkets are your best bet",
                anchor="The card on the file says \"Please bring this to the register with the products.\"</p>\n<!-- /wp:paragraph -->\n\n",
                alt="In-store notice: clear files are handed out at the service counter after payment", cap="Source: ",
                reps=[("*Information as of November 17, 2026.", "*Information as of November 18, 2026."),
                      ("<li>Sightings around Japan (as of Nov 17)</li>", "<li>Sightings around Japan (as of Nov 18)</li>"),
                      ("Take the clear file to the register with the products",
                       "Take the clear file to the register with the products (some stores hand it out at the service counter after payment)"),
                      ("That said, some AEON stores still did not have it on the 17th", "That said, some AEON stores still did not have it on the 18th")],
                key="as of 6:30 p.m., Nov 18"),
}


def cut(t, start, end):
    i = t.index(start)
    return i, t.index(end, i + 1)


def patch(pid, img_url):
    c = CFG[pid]
    t = w.get_post(pid)["content"]["raw"]
    n0 = len(t)
    for old, new in c["reps"] + [(c["anchor"], None)]:
        if t.count(old) != 1:
            raise SystemExit("{}: 見つからない({}) {}".format(pid, t.count(old), old[:60]))
        if new:
            t = t.replace(old, new)
    t = t.replace(c["anchor"], c["anchor"] + c["counter"](fig(img_url, c["alt"], c["cap"])))
    H3 = '<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{}'
    i, j = cut(t, H3.format(c["h_sight"]), H3.format(c["h_next"]))
    t = t[:i] + c["sight"]() + t[j:]
    m = re.search(r'(<h2 class="wp-block-heading">{}</h2>\n<!-- /wp:heading -->\n\n)<!-- wp:html -->.*?<!-- /wp:html -->\n\n'.format(c["summary"]), t, re.S)
    t = t[:m.end(1)] + b.checks(c["summ"]) + t[m.end():]
    print(pid, n0, "->", len(t))
    if APPLY:
        w.post("/posts/{}".format(pid), {"content": t})
        got = w.get_post(pid)["content"]["raw"]
        ok = c["key"] in got and img_url in got
        print(pid, "反映OK" if ok else "反映されてない！")
    else:
        open(os.path.join(os.environ.get("TEMP", "."), "bulg_{}.html".format(pid)), "w", encoding="utf-8").write(t)


img_url = "IMG_PLACEHOLDER"
if APPLY:
    mid = w.upload_media(POP_FILE, "KO1KEYZ×明治ブルガリアONE SHOT クリアファイルは会計後サービスカウンターで渡す売り場の貼り紙")
    img_url = w.get("/media/{}".format(mid))["source_url"]
    print("media", mid, img_url)
for pid in (15907, 15910, 15911):
    patch(pid, img_url)
