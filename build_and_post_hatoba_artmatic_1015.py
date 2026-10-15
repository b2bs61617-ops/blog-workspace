# -*- coding: utf-8 -*-
"""鳩場陸人(元・日プ新世界練習生、KO1KEYZ非メンバー)がJOY DANCE経由でARTMATIC COMPANYに最終合格(2026-10-14発表)。
一次情報:
- JOY DANCE JAPAN公式IG https://www.instagram.com/p/Ded7CdVEfgz/ (2026-10-14 17:10 JST、5枚組)
  キャプション「2026年9月、10月最終合格者（契約・輩出）です」
  2枚目 ARTMATIC COMPANY/ハトバ リクト、3枚目 事務所名非公開/ア** コ**、
  4枚目 THE 232 Entertainment(一般の受講生、名前は記事に出さない)、5枚目 NEED Entertainment/シ** カ**
- ARTMATIC COMPANY: 公式IG @artmatic_company のクレジット投稿(INFINITE 2025/3/6ミニアルバム5曲目「볼 수 있어 (Sad Loop)」、
  I:MOND「Wonderland」2025/2/14、SBS UNIVERSE LEAGUE「Don't Hit The Brakes」、SNH48 TEAMX「绝对领域」、
  チャ・ウジュのシングル、Rothy リメイク「파도」2026/7/7 Executive Producer 이현상)、
  KOCCA WelCon(ソウル城東区ソウルスプ2ギル45-1 B1、音楽IP事業・K-POP公演の企画制作 台湾/豪州/日本/南米)
- 日プ成績は自サイト7486/9433(鳩場=第1回順位発表97位、浅香=第3回順位発表26位)
- 「ア** コ**」=浅香孝太郎は未確定(本人IGは2026-05-30以降更新なし)。断定しない。
元ツイート(ファン)の画像は使わない。公式IGの埋め込みのみ。
"""
import sys

from build_and_post_uno_kaimu_sma_1010 import (ROOT, h2, h3, p, mark, html, minibox, infobox, table, barbox,
                                                leftbox, linkbox, summarybox, make_eyecatch, post_draft)

IG_POST = "https://www.instagram.com/p/Ded7CdVEfgz/"
ART_IG = "https://www.instagram.com/artmatic_company/"
HATOBA_IG = "https://www.instagram.com/poppo.ri09to/"


def ig_embed():
    return html(f'<blockquote class="instagram-media" data-instgrm-permalink="{IG_POST}?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" '
                'style="background:#FFF;border:0;border-radius:3px;box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);margin:1px auto;max-width:540px;min-width:326px;padding:0;width:calc(100% - 2px);">'
                f'<a href="{IG_POST}" target="_blank" rel="noopener">{IG_POST}</a></blockquote>\n'
                '<script async src="https://www.instagram.com/embed.js"></script>')


def map_embed(q):
    return html(f'<iframe src="https://maps.google.com/maps?q={q}&t=&z=14&ie=UTF8&iwloc=&output=embed" '
                'width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>')


MAP_SEONGSU = "%EC%84%9C%EC%9A%B8%EC%88%B22%EA%B8%B8%2045-1"  # 서울숲2길 45-1
MAP_KUSATSU = "%E6%BB%8B%E8%B3%80%E7%9C%8C%E8%8D%89%E6%B4%A5%E5%B8%82"  # 滋賀県草津市

JP_REL = [
    ("https://chomoand-1.com/hato_wiki-joy-dance-japan-3266", "鳩場陸人のwiki風経歴(高身長とダンス歴10年)"),
    ("https://chomoand-1.com/rikuto_no_school-3490", "鳩場陸人の学歴(滋賀県草津市の小学校・中学校)"),
    ("https://chomoand-1.com/asakakotaro_wiki-1228", "浅香孝太郎のwiki風経歴(バレエ歴16年以上・PICKUS出身)"),
    ("https://chomoand-1.com/hyeonseung-kotaro-kyoto-vlog-13897", "ヒョンスン＆孝太郎の京都Vlogの聖地"),
    ("https://chomoand-1.com/kaimu-uno-sony-music-artists-14519", "宇野海夢の事務所はソニー(日プ新世界の元練習生)"),
    ("https://chomoand-1.com/producejapan101_datsurakusha-7486", "【日プ新世界】脱落者一覧・全順位結果まとめ"),
]
KR_REL = [
    ("https://chomoand-1.com/ko/kaimu-uno-sony-music-artists-kr-14521", "우노 카이무, 소니 뮤직 아티스츠 소속! 탈락 후 근황은?"),
    ("https://chomoand-1.com/ko/hyeonseung-kotaro-kyoto-vlog-kr-13901", "현승 & 코타로 교토 브이로그 성지는?"),
]
EN_REL = [
    ("https://chomoand-1.com/en/kaimu-uno-sony-music-artists-en-14522", "Kaimu Uno signs with Sony Music Artists"),
    ("https://chomoand-1.com/en/hyeonseung-kotaro-kyoto-vlog-en-13902", "Hyeonseung & Kotaro's Kyoto vlog spots"),
]

# ============================== JP ==============================
JP_TITLE = "【日プ新世界】鳩場陸人の事務所はARTMATIC！孝太郎も？"
JP_SLUG = "rikuto-hatoba-artmatic-company"

JP_CONTENT = "\n\n".join([
    p("『PRODUCE 101 JAPAN 新世界(日プ新世界・日プ4)』に出演していた鳩場陸人(はとば・りくと)さんの進路が明らかになりました。<br>\n"
      f"2026年10月14日、鳩場さんが通っていたK-POPオーディション専門スクール「JOY DANCE」が、{mark('韓国の音楽制作会社「ARTMATIC COMPANY(アートマティック・カンパニー)」に鳩場さんが最終合格したこと', True)}を公式Instagramで発表しています。<br>\n"
      "同じ発表では、事務所名を伏せたまま「ア** コ**」という名前の合格者も紹介されていました。<br>\n"
      "この記事では、ARTMATIC COMPANYがどんな会社なのか、鳩場さんのプロフィールと日プでの歩み、そして伏せ字の合格者が浅香孝太郎さんなのかを整理します。"),
    infobox("JOY DANCEの最終合格発表の基本情報", [
        ("発表日", "2026年10月14日"),
        ("発表した場所", "JOY DANCE JAPAN公式Instagram(@joydance_japan)"),
        ("発表の内容", "2026年9月・10月のオーディション最終合格者(契約・輩出)"),
        ("鳩場陸人さんの合格先", "ARTMATIC COMPANY(韓国・ソウル)"),
        ("「ア** コ**」さんの合格先", "事務所名は非公開"),
        ("日プ新世界での最終順位", "鳩場さん97位(第1回順位発表式で脱落)"),
    ]),
    barbox("この記事でわかること", [
        "鳩場陸人さんの合格先",
        "ARTMATIC COMPANYはどんな会社？",
        "鳩場陸人さんのプロフィール",
        "日プ新世界での成績",
        "「ア** コ**」は浅香孝太郎さん？",
        "JOY DANCEはどんなスクール？",
    ]),

    h2("鳩場陸人の合格先はどこ？"),
    minibox([("合格先：", "ARTMATIC COMPANY(アートマティック・カンパニー)"), ("発表：", "2026年10月14日、JOY DANCE JAPAN公式Instagram")]),
    p("鳩場さんの名前が載ったのは、JOY DANCE JAPANが10月14日の夕方に投稿した「9月・10月 オーディション合格実況」です。<br>\n"
      "5枚の画像のうち2枚目に、ARTMATIC COMPANYのロゴと「ハトバ リクト」というカタカナの名前が大きく並んでいます。"),
    ig_embed(),
    p("投稿の文章には「2026年9月、10月最終合格者（契約・輩出）です」と書かれており、オーディションの途中経過ではなく<strong>最終合格＝契約まで進んだ人の発表</strong>であることが分かります。<br>\n"
      "合格者は全部で4人で、鳩場さんのほかに、事務所名非公開の「ア** コ**」さん、THE 232 Entertainmentの合格者、NEED Entertainmentの「シ** カ**」さんが紹介されていました。<br>\n"
      "フルネームと事務所名の両方が公開されているのは鳩場さんを含む2人だけで、残りは本人の希望などで伏せ字になっているとみられます。"),
    p("鳩場さんは日プ新世界に出る前から、JOY DANCEの大阪校に通っていたことが分かっています。<br>\n"
      "番組を終えたあとも同じスクールでオーディションを受け続け、約4か月で韓国の会社との契約をつかんだことになります。"),

    h2("ARTMATIC COMPANYはどんな会社？"),
    minibox([("所在地：", "韓国・ソウル市城東区(ソウルの森の近く)"), ("主な事業：", "楽曲制作・音楽出版・アーティストのマネジメント")]),
    p("ARTMATIC COMPANY(アートマティック・カンパニー)は、韓国・ソウルを拠点にする音楽制作会社です。<br>\n"
      "プロデューサーのイ・ヒョンサンさんが立ち上げた会社で、作曲家やアレンジャーが所属し、楽曲制作と音楽出版をメインにしながら、アーティストのマネジメントも手がけています。<br>\n"
      "韓国コンテンツ振興院のデータベースでは、所在地はソウル市城東区のソウルの森(ソウルスプ)のすぐそば、おしゃれなカフェが集まる聖水(ソンス)エリアにあたります。"),
    map_embed(MAP_SEONGSU),
    p("公式Instagramを見てみると、これまでにK-POPやC-POPのさまざまなアーティストに曲を提供していることが分かります。<br>\n"
      "主な実績をまとめると次のとおりです。"),
    table(["時期", "アーティスト", "ARTMATICの関わり"], [
        ["2025年1月ごろ", "UNIVERSE LEAGUE(SBSのボーイズグループ選抜番組)", "1曲目「Don't Hit The Brakes」の作曲に参加"],
        ["2025年1月ごろ", "SNH48のユニット「TEAMX」(中国)", "「绝对领域」の作曲・編曲"],
        ["2025年2月14日", "I:MOND(ガールズグループ)", "1stミニアルバムの「Wonderland」の作詞・作曲"],
        ["2025年3月6日", "INFINITE", "ミニアルバムの5曲目「볼 수 있어(ボル ス イッソ(会えるよ)) (Sad Loop)」の作曲・編曲"],
        ["2025年〜2026年", "チャ・ウジュ(ソロ歌手)", "シングルを継続してリリース"],
        ["2026年7月7日", "Rothy(ロシ)", "リメイク曲「파도(パド(波))」をプロデュース"],
    ]),
    p(f"なかでも、2世代アイドルの代表格であるINFINITEのアルバムに{mark('自社チームで作った曲が収録されている')}のは大きな実績です。<br>\n"
      "このほか、台湾・オーストラリア・日本・南米でのK-POP公演の企画にも関わっていると紹介されています。"),
    p("一方で、2026年10月時点ではARTMATIC COMPANYからデビューしたアイドルグループは見当たりません。<br>\n"
      "楽曲制作を強みとする会社が練習生と契約したことから、新しいボーイズグループの準備を進めている可能性もありそうです。<br>\n"
      "鳩場さんがどんな形でデビューを目指すのかはまだ発表されていないため、今後の公式発表に注目です。"),

    h2("鳩場陸人のプロフィール"),
    minibox([("出身：", "滋賀県"), ("年齢：", "17歳(2026年10月時点)"), ("身長：", "182cm")]),
    p("鳩場さんは、日プ新世界の練習生の中でも年少組にあたる2009年生まれです。<br>\n"
      "番組で公開された公式プロフィールをもとに整理すると、次のとおりです。"),
    infobox("鳩場陸人さんのプロフィール", [
        ("名前", "鳩場陸人(はとば・りくと)/HATOBA RIKUTO"),
        ("生年月日", "2009年8月31日"),
        ("年齢", "17歳(2026年10月時点)"),
        ("出身地", "滋賀県(草津市の小学校出身とみられる)"),
        ("身長", "182cm"),
        ("MBTI", "ENFJ(主人公型)"),
        ("趣味", "音楽を聴くこと"),
        ("特技", "書道"),
        ("私を表すキーワード", "若い"),
        ("通っていたスクール", "JOY DANCE JAPAN 大阪校"),
        ("合格先", "ARTMATIC COMPANY(2026年10月発表)"),
    ]),
    p(f"17歳で182cmという{mark('恵まれたスタイル')}は、番組の放送中から目を引いていました。<br>\n"
      "ダンス歴は約10年とされ、2025年の夏には韓国の芸能高校として知られるハンリム芸能芸術学校のサマーキャンプにも参加しています。<br>\n"
      "小学2年生のころには書道の作品が新聞に載ったこともあり、ダンスとは別に、じっくり集中する特技を持っているのも鳩場さんらしいところです。"),
    p("出身の滋賀県草津市は、大阪のスクールにも通える距離にあります。<br>\n"
      "学校のことは<a href=\"https://chomoand-1.com/rikuto_no_school-3490\">鳩場陸人の学歴の記事</a>で、経歴は<a href=\"https://chomoand-1.com/hato_wiki-joy-dance-japan-3266\">鳩場陸人のwiki風経歴の記事</a>でくわしく紹介しています。"),
    map_embed(MAP_KUSATSU),

    h2("日プ新世界での鳩場陸人の成績は？"),
    minibox([("最終順位：", "97位"), ("脱落：", "第1回順位発表式")]),
    p("鳩場さんは、日プ新世界で第1回順位発表式の97位となり、上位50人に入れず脱落しました。<br>\n"
      "放送で映る時間は多くありませんでしたが、テーマソングの推しカメラでは、長い手足を生かした大きな振りと表情づくりが印象に残った人も多かったはずです。"),
    p("2026年6月に番組の放送が終わってから約4か月で、韓国の会社との契約にこぎつけたことになります。<br>\n"
      "まだ17歳という若さを考えると、これから韓国で練習を重ねていく時間も十分にあります。<br>\n"
      "ほかの練習生の順位は<a href=\"https://chomoand-1.com/producejapan101_datsurakusha-7486\">日プ新世界の脱落者一覧</a>で確認できます。"),
    p("日プ新世界の元練習生では、10月10日に宇野海夢さんもSony Music Artistsへの所属を発表しています。<br>\n"
      "番組を終えた練習生たちが、日本と韓国のそれぞれで新しい道を見つけ始めています(<a href=\"https://chomoand-1.com/kaimu-uno-sony-music-artists-14519\">宇野海夢さんの所属の記事</a>)。"),

    h2("「ア** コ**」は浅香孝太郎？"),
    minibox([("合格先：", "事務所名非公開"), ("本人：", "名前も伏せ字のため確定していない")]),
    p("同じ発表の3枚目には、事務所名を「非公開」とした「ア** コ**」さんの合格も載っていました。<br>\n"
      f"日プ新世界の練習生でこの伏せ字にぴったり当てはまるのが{mark('浅香孝太郎(アサカ コウタロウ)さん')}で、鳩場さんと並んで発表されたこともあり、もしかして孝太郎さんでは？と注目が集まっています。"),
    p("ただし、JOY DANCEは日プ出身者だけでなく、多くの一般の受講生が通うスクールです。<br>\n"
      "孝太郎さんはもともと「K-POP ACADEMY FANCY 神戸三宮校」の出身として知られており、JOY DANCEに通っていたことは本人から明かされていません。<br>\n"
      "本人のInstagramも2026年5月30日の投稿を最後に更新がなく、<strong>現時点では孝太郎さんだと確定できる情報はありません</strong>。"),
    p("孝太郎さんは、韓国のオーディション番組「Fan Pick」を経てボーイズグループPICKUS(ピカス)としてデビューし、その後「PROJECT 7」、日プ新世界と挑戦を続けてきました。<br>\n"
      "日プ新世界では第3回順位発表式で26位となり、ファイナルに進む22人にあと一歩届きませんでした。<br>\n"
      "4か国語を話せて韓国での活動経験もあるだけに、韓国の事務所と契約したとしても不思議ではありません。<br>\n"
      "もし本人の口から発表があれば、追記していきます。"),
    linkbox("浅香孝太郎さんの関連記事", [
        ("https://chomoand-1.com/asakakotaro_wiki-1228", "浅香孝太郎のwiki風経歴(バレエ歴16年以上・PICKUS出身)"),
        ("https://chomoand-1.com/hyeonseung-kotaro-kyoto-vlog-13897", "ヒョンスン＆孝太郎の京都Vlogの聖地"),
        ("https://chomoand-1.com/ko-taro-chrome-hearts-8177", "浅香孝太郎のピアスのブランド(クロムハーツ説)"),
    ]),

    h2("JOY DANCEはどんなスクール？"),
    minibox([("拠点：", "韓国(ソウル江南ほか)、日本(東京・大阪)"), ("特徴：", "K-POPオーディション専門のアカデミー")]),
    p("JOY DANCEは、韓国で2003年からオーディション対策を行ってきたK-POPアイドル養成アカデミーです。<br>\n"
      "日本では「JOY DANCE TOKYO・OSAKA」として東京と大阪で教室を開いており、鳩場さんは大阪校に通っていました。"),
    leftbox("JOY DANCEの出身として紹介されている主なアイドル(公式発表より)",
            '<p style="margin:0;">BTS j-hope、STAYC ユン、WINNER ジヌ、ATEEZ ユンホ・ミンギ など、105人以上</p>'),
    p("公式の案内によると、1対1のコンサルティングや毎月の評価・フィードバックが受けられ、韓国の事務所のオーディションに直接つながる仕組みが強みです。<br>\n"
      "今回のように、毎月の合格者を事務所のロゴ付きで発表しているのも特徴で、9月・10月だけでも4人が契約までたどり着いています。<br>\n"
      "ほかの練習生の通っていたスクールは<a href=\"https://chomoand-1.com/101_dance-school-6278\">日プ新世界の練習生の出身ダンススクール一覧</a>にまとめています。"),

    h2("鳩場陸人の今後の活動は？"),
    minibox([("デビュー：", "未発表(2026年10月15日時点)"), ("チェック先：", "本人のInstagram、ARTMATIC COMPANYの公式Instagram")]),
    p("2026年10月15日時点では、鳩場さんが練習生としてグループのデビューを目指すのか、どんな形で活動していくのかはまだ発表されていません。<br>\n"
      f"最新の情報は、本人のInstagram(<a href=\"{HATOBA_IG}\" target=\"_blank\" rel=\"noopener\">@poppo.ri09to</a>)や、<a href=\"{ART_IG}\" target=\"_blank\" rel=\"noopener\">ARTMATIC COMPANYの公式Instagram</a>で発表されるとみられます。"),
    p("楽曲づくりに強い会社に入ったことで、歌やダンスだけでなく、音楽そのものに深く関わる経験も積めそうです。<br>\n"
      "17歳での韓国挑戦が、どんなデビューにつながるのか楽しみなところです。"),

    h2("まとめ"),
    summarybox([
        "鳩場陸人さんは、JOY DANCEのオーディションで韓国のARTMATIC COMPANYに最終合格した(2026年10月14日発表)",
        "ARTMATIC COMPANYはソウル・聖水エリアの音楽制作会社で、INFINITEやI:MONDなどに楽曲を提供している",
        "鳩場さんは滋賀県出身の17歳、身長182cm。日プ新世界では第1回順位発表式で97位となり脱落",
        "同じ発表の「ア** コ**」さん(事務所名非公開)は浅香孝太郎さんの可能性があるが、確定していない",
        "デビューの時期や形はまだ発表されていない",
    ]),
    p("日プ新世界のあと、地道にオーディションを受け続けて契約をつかんだ鳩場さん。<br>\n"
      "番組のころから応援していた方も、これから知ったという方も、韓国での新しい挑戦をぜひ一緒に見守っていきましょう！"),
    linkbox("鳩場陸人・日プ新世界の関連記事", JP_REL),
])

JP_SUMMARY = ("日プ新世界に出演した鳩場陸人さんが、JOY DANCEのオーディションで韓国の音楽制作会社ARTMATIC COMPANYに最終合格。"
              "どんな会社なのか、同時に発表された「ア** コ**」さんは浅香孝太郎さんなのかをまとめました。")

# ============================== KR ==============================
KR_TITLE = "[닛프 신세계] 하토바 리쿠토, 아트매틱 컴퍼니 최종 합격! 코타로도?"
KR_SLUG = f"{JP_SLUG}-kr"

KR_CONTENT = "\n\n".join([
    p("『PRODUCE 101 JAPAN 新世界(닛프 신세계・닛프4)』에 출연했던 하토바 리쿠토(鳩場陸人)의 새로운 진로가 알려졌습니다.<br>\n"
      f"2026년 10월 14일, 그가 다니던 K-POP 오디션 전문 아카데미 'JOY DANCE'가 공식 Instagram을 통해 {mark('하토바 리쿠토가 한국 음악 제작사 아트매틱 컴퍼니(ARTMATIC COMPANY)에 최종 합격했다', True)}고 발표했습니다.<br>\n"
      "같은 발표에는 소속사 이름을 비공개로 한 'ア** コ**(아** 코**)'라는 합격자도 소개되었습니다.<br>\n"
      "이 글에서는 아트매틱 컴퍼니가 어떤 회사인지, 하토바 리쿠토의 프로필과 닛프 성적, 그리고 비공개 합격자가 아사카 코타로인지 정리합니다."),
    infobox("JOY DANCE 최종 합격 발표 기본 정보", [
        ("발표일", "2026년 10월 14일"),
        ("발표 채널", "JOY DANCE JAPAN 공식 Instagram(@joydance_japan)"),
        ("내용", "2026년 9・10월 오디션 최종 합격자(계약)"),
        ("하토바 리쿠토 합격처", "ARTMATIC COMPANY(서울)"),
        ("'ア** コ**' 합격처", "소속사 비공개"),
        ("닛프 신세계 최종 순위", "하토바 97위(1차 순위 발표식 탈락)"),
    ]),
    h2("하토바 리쿠토의 합격처는 어디?"),
    minibox([("합격처: ", "ARTMATIC COMPANY(아트매틱 컴퍼니)"), ("발표: ", "2026년 10월 14일, JOY DANCE JAPAN 공식 Instagram")]),
    p("JOY DANCE JAPAN이 10월 14일 저녁에 올린 '9월・10월 오디션 합격 실황' 5장 중 두 번째 이미지에 아트매틱 컴퍼니 로고와 'ハトバ リクト(하토바 리쿠토)'라는 이름이 실렸습니다."),
    ig_embed(),
    p("게시물에는 '2026년 9월, 10월 최종 합격자(계약・배출)'라고 적혀 있어, <strong>계약까지 진행된 최종 합격 발표</strong>임을 알 수 있습니다.<br>\n"
      "합격자는 모두 4명으로, 하토바 외에 소속사 비공개 'ア** コ**', THE 232 Entertainment 합격자, NEED Entertainment의 'シ** カ**'가 소개되었습니다.<br>\n"
      "그는 닛프 출연 전부터 JOY DANCE 오사카점에 다녔으며, 프로그램 종료 후에도 같은 아카데미에서 오디션에 도전해 종영 약 4개월 만에 한국 회사와의 계약을 따냈습니다."),
    h2("아트매틱 컴퍼니는 어떤 회사?"),
    minibox([("위치: ", "서울 성동구 서울숲2길(성수 지역)"), ("주요 사업: ", "음악 제작・음악 퍼블리싱・아티스트 매니지먼트")]),
    p("아트매틱 컴퍼니는 프로듀서 이현상이 이끄는 서울의 음악 제작사입니다.<br>\n"
      "작곡가와 편곡가가 소속되어 있으며, 음악 제작과 퍼블리싱을 중심으로 아티스트 매니지먼트도 하고 있습니다."),
    map_embed(MAP_SEONGSU),
    table(["시기", "아티스트", "아트매틱의 참여"], [
        ["2025년 1월경", "UNIVERSE LEAGUE(SBS)", "'Don't Hit The Brakes' 작곡 참여"],
        ["2025년 1월경", "SNH48 유닛 TEAMX(중국)", "'绝对领域' 작곡・편곡"],
        ["2025년 2월 14일", "아이몬드(I:MOND)", "'Wonderland' 작사・작곡"],
        ["2025년 3월 6일", "인피니트(INFINITE)", "미니앨범 5번 트랙 '볼 수 있어 (Sad Loop)' 작곡・편곡"],
        ["2025~2026년", "차우주", "싱글 연속 발매"],
        ["2026년 7월 7일", "로시(Rothy)", "리메이크 '파도' 프로듀스"],
    ]),
    p(f"특히 {mark('인피니트 앨범에 자체 팀이 만든 곡이 수록된 것')}은 큰 실적입니다.<br>\n"
      "다만 2026년 10월 기준 이 회사에서 데뷔한 아이돌 그룹은 확인되지 않아, 새로운 보이그룹을 준비하고 있을 가능성도 있어 보입니다."),
    h2("하토바 리쿠토 프로필"),
    minibox([("출신: ", "일본 시가현"), ("나이: ", "17세(2026년 10월 기준)"), ("키: ", "182cm")]),
    infobox("하토바 리쿠토 프로필", [
        ("이름", "하토바 리쿠토(鳩場陸人)/HATOBA RIKUTO"),
        ("생년월일", "2009년 8월 31일"),
        ("나이", "17세(2026년 10월 기준)"),
        ("출신지", "일본 시가현"),
        ("키", "182cm"),
        ("MBTI", "ENFJ"),
        ("취미", "음악 듣기"),
        ("특기", "서예"),
        ("아카데미", "JOY DANCE JAPAN 오사카점"),
        ("합격처", "ARTMATIC COMPANY(2026년 10월 발표)"),
    ]),
    p("댄스 경력은 약 10년으로, 2025년 여름에는 한림연예예술고등학교 서머캠프에도 참가했습니다.<br>\n"
      "초등학교 2학년 때는 서예 작품이 신문에 실린 적도 있습니다."),
    h2("닛프 신세계 성적은?"),
    minibox([("최종 순위: ", "97위"), ("탈락: ", "1차 순위 발표식")]),
    p("하토바 리쿠토는 1차 순위 발표식에서 97위로 상위 50명에 들지 못해 탈락했습니다.<br>\n"
      "2026년 6월 프로그램 종영 후 약 4개월 만에 한국 회사와 계약했고, 아직 17세인 만큼 앞으로 연습할 시간도 충분합니다.<br>\n"
      "닛프 신세계 출신으로는 10월 10일 우노 카이무가 Sony Music Artists 소속을 발표하기도 했습니다."),
    h2("'ア** コ**'는 아사카 코타로?"),
    minibox([("합격처: ", "소속사 비공개"), ("본인: ", "이름도 가려져 있어 확정되지 않음")]),
    p(f"같은 발표의 세 번째 이미지에는 소속사 '비공개'인 'ア** コ**' 합격자가 실렸습니다.<br>\n"
      f"닛프 신세계 연습생 중 이 이니셜에 맞는 사람은 {mark('아사카 코타로(アサカ コウタロウ)')}여서 주목받고 있습니다.<br>\n"
      "다만 JOY DANCE에는 일반 수강생도 많이 다니고, 코타로는 'K-POP ACADEMY FANCY 고베산노미야점' 출신으로 알려져 있습니다.<br>\n"
      "본인 Instagram도 2026년 5월 30일 이후 업데이트가 없어 <strong>현재로서는 코타로라고 확정할 수 있는 정보는 없습니다</strong>."),
    p("코타로는 'Fan Pick'을 거쳐 PICKUS로 데뷔했고, 이후 'PROJECT 7'과 닛프 신세계에 도전했습니다.<br>\n"
      "닛프 신세계에서는 3차 순위 발표식에서 26위로 아쉽게 파이널 진출에 실패했습니다."),
    h2("JOY DANCE는 어떤 아카데미?"),
    minibox([("거점: ", "한국(강남 등), 일본(도쿄・오사카)"), ("특징: ", "K-POP 오디션 전문")]),
    p("JOY DANCE는 2003년부터 오디션 준비를 해 온 K-POP 아이돌 양성 아카데미입니다.<br>\n"
      "공식 안내에 따르면 BTS 제이홉, STAYC 윤, WINNER 진우, ATEEZ 윤호・민기 등 105명 이상의 아이돌을 배출했습니다."),
    h2("정리"),
    summarybox([
        "하토바 리쿠토는 JOY DANCE 오디션을 통해 아트매틱 컴퍼니에 최종 합격했다(2026년 10월 14일 발표)",
        "아트매틱 컴퍼니는 서울 성수 지역의 음악 제작사로, 인피니트・아이몬드 등에 곡을 제공했다",
        "하토바는 시가현 출신 17세, 키 182cm. 닛프 신세계 1차 순위 발표식에서 97위로 탈락",
        "같은 발표의 'ア** コ**'(소속사 비공개)는 아사카 코타로일 가능성이 있지만 확정되지 않았다",
    ]),
    p("17세에 한국에서 새로운 도전을 시작한 하토바 리쿠토의 앞날을 함께 응원해요!"),
    linkbox("관련 글", KR_REL),
])

KR_SUMMARY = ("닛프 신세계에 출연한 하토바 리쿠토가 JOY DANCE 오디션을 통해 한국 음악 제작사 아트매틱 컴퍼니에 최종 합격했습니다. "
              "어떤 회사인지, 함께 발표된 'ア** コ**'가 아사카 코타로인지 정리했습니다.")

# ============================== EN ==============================
EN_TITLE = "Rikuto Hatoba Passes ARTMATIC COMPANY's Final Audition! Is Kotaro Asaka Next?"
EN_SLUG = f"{JP_SLUG}-en"

EN_CONTENT = "\n\n".join([
    p("Rikuto Hatoba (鳩場陸人), who appeared on PRODUCE 101 JAPAN SHINSEKAI, has found his next step.<br>\n"
      f"On October 14, 2026, the K-pop audition academy JOY DANCE announced on Instagram that {mark('Rikuto passed the final audition of the Korean music company ARTMATIC COMPANY', True)}.<br>\n"
      "The same post also listed a second passer, \"ア** コ** (A** Ko**),\" whose agency was kept private.<br>\n"
      "This article covers what ARTMATIC COMPANY is, Rikuto's profile and journey on the show, and whether the hidden name could be Kotaro Asaka."),
    infobox("JOY DANCE announcement at a glance", [
        ("Date", "October 14, 2026"),
        ("Where", "JOY DANCE JAPAN's Instagram (@joydance_japan)"),
        ("What", "Final audition passers (contracts) for September and October 2026"),
        ("Rikuto's company", "ARTMATIC COMPANY (Seoul)"),
        ("\"ア** コ**\"'s company", "Not disclosed"),
        ("Rikuto's final rank on the show", "97th (eliminated at the 1st ranking ceremony)"),
    ]),
    h2("Which company did Rikuto Hatoba pass?"),
    minibox([("Company: ", "ARTMATIC COMPANY"), ("Announced: ", "Oct 14, 2026 on JOY DANCE JAPAN's Instagram")]),
    p("JOY DANCE JAPAN posted five images of its September-October audition results. The second one shows the ARTMATIC COMPANY logo with the name \"ハトバ リクト (Hatoba Rikuto).\""),
    ig_embed(),
    p("The caption describes them as <strong>final passers who signed contracts</strong>, not passers of an early round.<br>\n"
      "Four people were listed: Rikuto, \"ア** コ**\" (agency undisclosed), a passer for THE 232 Entertainment, and \"シ** カ**\" for NEED Entertainment.<br>\n"
      "Rikuto attended JOY DANCE's Osaka branch before the show, and about four months after the show ended in June 2026 he landed a contract with a Korean company."),
    h2("What kind of company is ARTMATIC COMPANY?"),
    minibox([("Location: ", "Seongsu area, Seongdong-gu, Seoul"), ("Business: ", "Music production, publishing and artist management")]),
    p("ARTMATIC COMPANY is a Seoul music production company led by producer Lee Hyunsang.<br>\n"
      "Its team of composers and arrangers focuses on producing and publishing music, and the company also manages artists."),
    map_embed(MAP_SEONGSU),
    table(["When", "Artist", "ARTMATIC's role"], [
        ["Around Jan 2025", "UNIVERSE LEAGUE (SBS)", "Co-composed \"Don't Hit The Brakes\""],
        ["Around Jan 2025", "TEAMX, a unit of SNH48 (China)", "Composed and arranged \"绝对领域\""],
        ["Feb 14, 2025", "I:MOND", "Wrote and composed \"Wonderland\""],
        ["Mar 6, 2025", "INFINITE", "Composed and arranged track 5 of the mini album, \"볼 수 있어 (Sad Loop)\""],
        ["2025-2026", "Cha Woo Joo", "Released a series of singles"],
        ["Jul 7, 2026", "Rothy", "Produced the remake \"파도 (Wave)\""],
    ]),
    p(f"Having {mark('a song by its in-house team on an INFINITE album')} stands out among these credits.<br>\n"
      "As of October 2026, no idol group has debuted under the company, so it may be preparing a new boy group."),
    h2("Rikuto Hatoba's profile"),
    minibox([("From: ", "Shiga Prefecture, Japan"), ("Age: ", "17 (as of October 2026)"), ("Height: ", "182cm")]),
    infobox("Rikuto Hatoba profile", [
        ("Name", "Rikuto Hatoba (鳩場陸人)"),
        ("Birthday", "August 31, 2009"),
        ("Age", "17 (as of October 2026)"),
        ("Hometown", "Shiga Prefecture, Japan"),
        ("Height", "182cm"),
        ("MBTI", "ENFJ"),
        ("Hobby", "Listening to music"),
        ("Skill", "Calligraphy"),
        ("Academy", "JOY DANCE JAPAN Osaka"),
        ("Company", "ARTMATIC COMPANY (announced October 2026)"),
    ]),
    p("He has about ten years of dance experience and joined the summer camp of Hanlim Multi Art School in Korea in 2025.<br>\n"
      "As a second grader, one of his calligraphy works was even printed in a newspaper."),
    h2("How did he do on PRODUCE 101 JAPAN SHINSEKAI?"),
    minibox([("Final rank: ", "97th"), ("Eliminated: ", "1st ranking ceremony")]),
    p("Rikuto ranked 97th at the first ranking ceremony and missed the top 50.<br>\n"
      "About four months after the show ended, he has a contract in Korea, and at 17 he has plenty of time to keep training.<br>\n"
      "Another former trainee, Kaimu Uno, announced on October 10 that he joined Sony Music Artists."),
    h2("Is \"ア** コ**\" Kotaro Asaka?"),
    minibox([("Company: ", "Not disclosed"), ("Identity: ", "Not confirmed, as the name is hidden")]),
    p(f"The third image shows a passer named \"ア** コ**\" with the agency marked as private.<br>\n"
      f"Among the show's trainees, {mark('Kotaro Asaka (アサカ コウタロウ)')} fits these initials, which has drawn attention.<br>\n"
      "However, JOY DANCE has many students outside the show, and Kotaro is known as a graduate of a different school, K-POP ACADEMY FANCY in Kobe.<br>\n"
      "His Instagram hasn't been updated since May 30, 2026, so <strong>there is no confirmation that it is him</strong>."),
    p("Kotaro debuted with PICKUS after the Korean show \"Fan Pick,\" then took on PROJECT 7 and PRODUCE 101 JAPAN SHINSEKAI, where he finished 26th at the third ranking ceremony, just short of the final 22."),
    h2("What is JOY DANCE?"),
    minibox([("Locations: ", "Korea (Gangnam and more), Japan (Tokyo and Osaka)"), ("Focus: ", "K-pop audition training")]),
    p("JOY DANCE is a K-pop idol academy that has offered audition training since 2003.<br>\n"
      "According to the academy, it has produced more than 105 idols, including BTS's j-hope, STAYC's Yoon, WINNER's Jinu, and ATEEZ's Yunho and Mingi."),
    h2("Summary"),
    summarybox([
        "Rikuto Hatoba passed ARTMATIC COMPANY's final audition through JOY DANCE (announced Oct 14, 2026)",
        "ARTMATIC COMPANY is a music production company in Seongsu, Seoul, with credits for INFINITE, I:MOND and more",
        "Rikuto is 17, from Shiga, 182cm tall, and was eliminated at 97th on the show",
        "\"ア** コ**\" (agency undisclosed) may be Kotaro Asaka, but this is not confirmed",
    ]),
    p("Let's cheer Rikuto on as he begins his new challenge in Korea at 17!"),
    linkbox("Related articles", EN_REL),
])

EN_SUMMARY = ("Former PRODUCE 101 JAPAN SHINSEKAI trainee Rikuto Hatoba passed ARTMATIC COMPANY's final audition through JOY DANCE. "
              "Here's what the company is and whether the hidden passer \"ア** コ**\" is Kotaro Asaka.")

if __name__ == "__main__":
    if "--dry" in sys.argv:
        import re
        for name, c in [("JP", JP_CONTENT), ("KR", KR_CONTENT), ("EN", EN_CONTENT)]:
            t = re.sub(r"<!--.*?-->|<script.*?</script>|<[^>]+>", "", c, flags=re.S)
            print(name, "chars:", len(re.sub(r"\s", "", t)))
        print("JP title len", len(JP_TITLE))
        sys.exit()

    JP_EYECATCH_ID = make_eyecatch(
        ["--top", "PRODUCE 101 新世界", "--main", "鳩場 陸人", "--bottom", "ARTMATICに最終合格！", "--bottom", "孝太郎も？"],
        ROOT / "images" / "hatoba_artmatic_1015_eyecatch.png")
    print("JP_EYECATCH_ID", JP_EYECATCH_ID)
    jp = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, "ja", [4, 62], JP_EYECATCH_ID, JP_SUMMARY)
    print("JP_POST_ID", jp["id"], jp["slug"])

    KR_EYECATCH_ID = make_eyecatch(
        ["--top", "PRODUCE 101 新世界", "--main", "하토바 리쿠토", "--bottom", "아트매틱 최종 합격!", "--bottom", "코타로도?", "--lang", "kr"],
        ROOT / "images" / "hatoba_artmatic_1015_eyecatch_kr.png")
    kr = post_draft(KR_TITLE, KR_CONTENT, KR_SLUG, "ko", [72, 70], KR_EYECATCH_ID, KR_SUMMARY)
    print("KR_POST_ID", kr["id"], kr["slug"])

    en = post_draft(EN_TITLE, EN_CONTENT, EN_SLUG, "en", [116, 112], JP_EYECATCH_ID, EN_SUMMARY)
    print("EN_POST_ID", en["id"], en["slug"])
