# -*- coding: utf-8 -*-
"""髙城暖人・リュウ・カイチ(元・日プ新世界練習生、KO1KEYZ非メンバー)が長良グループに所属(2026-10-15)。
一次情報:
- 長良プロダクション公式サイト(WP) talent/harutotakagi(id31768)・talent/lukaichi(id31767) 2026-10-15 10:00作成
  髙城: 所属 長良マネジメント/東京都/2003-10-26/176cm/趣味 散歩/特技 テニス/IG haruto__1026
  カイチ: 所属 長良マネジメント/愛知県/2004-02-13/184cm/趣味 アニメ、楽器/特技 自分の良いところをいっぱい言える所/IG kaichiliu.my_shinsekai_
- 髙城本人IG https://www.instagram.com/p/Def9P1Zs21O/ (2026-10-15 12:09 JST)「長良プロダクションに所属することになりました」
  カイチ本人のIG(最終投稿6/13)・X(@1ka_liu)には10/15時点で報告の投稿なし
  →10/16 10:32 JST、カイチ本人IG https://www.instagram.com/p/DeiVvAlS0in/ (nagara.sparkleclubとの共同投稿)で「ご報告」
    「長良プロダクション様と契約」/アイドルという職業に燃え尽き、少し気持ちが離れていた/長良の熱意でもう一度頑張ろうと思えた
    (10/16リライト: 公開済みなのでタイトル・スラッグは変えず本文のみ更新。`--update`)
- 長良公式ニュース https://www.nagarapro.co.jp/31804/ (10/15 12:00)「NAGARA SPARKLE CLUB」オープン
  対象: 田村継・伊勢之佑人・新田見直登・髙城暖人・リュウ・カイチ・黒木歩夢・鈴木恒守・松永幸士(FCブログ一覧には渡邊景日も)
- 長良グループ公式X https://twitter.com/nagaragroup/status/2110566703012921793 (10/15 12:01 JST)
- FC https://nagarasparkleclub.bitfan.id/ (Bitfan) レギュラー(ベーシック)330円/プレミアム550円 月額税込・入会金なし・更新日は毎月1日
  決済 クレカ/キャリア/あと払いペイディ。プレミアム限定=ライブ配信アーカイブ・プライベートチャット(準備中)・限定デザイン会員証
  10/15に髙城の「自己紹介✨」ブログ(レギュラー会員以上)が公開
- 日プ成績は自サイト5241/5733/7622/7482/7486/9433:
  2人とも練習生候補で脱落候補→オンライン投票でFクラス昇格。髙城=M!LK「イイじゃん」、カイチ=PSYCHIC FEVER「Paradise」
  GB「Love seeker」1組リーダー=カイチ(ボーカル3 12票)、2組リーダー=髙城(ラップ1 14票)、1組595×2組436で1組勝利
  髙城=第1回順位発表70位で脱落。カイチ=第2回31位で通過→PB「ベテルギウス」チーム内3位→コンセプト「DREAMER」→第3回34位で脱落
元ツイート(ファン)の画像は使わない。公式X・本人IGの埋め込みのみ。
"""
import sys

from build_and_post_uno_kaimu_sma_1010 import (ROOT, h2, h3, p, mark, html, minibox, infobox, table, barbox,
                                                leftbox, linkbox, summarybox, make_eyecatch, post_draft)

HARUTO_IG_POST = "https://www.instagram.com/p/Def9P1Zs21O/"
KAICHI_IG_POST = "https://www.instagram.com/p/DeiVvAlS0in/"
HARUTO_IG = "https://www.instagram.com/haruto__1026/"
KAICHI_IG = "https://www.instagram.com/kaichiliu.my_shinsekai_/"
NAGARA_X = "https://twitter.com/nagaragroup/status/2110566703012921793"
NAGARA_NEWS = "https://www.nagarapro.co.jp/31804/"
HARUTO_PAGE = "https://www.nagarapro.co.jp/talent/harutotakagi/"
KAICHI_PAGE = "https://www.nagarapro.co.jp/talent/lukaichi/"
FC_URL = "https://nagarasparkleclub.bitfan.id/"


def a(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'


def ig_embed(post=HARUTO_IG_POST):
    return html(f'<blockquote class="instagram-media" data-instgrm-permalink="{post}?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" '
                'style="background:#FFF;border:0;border-radius:3px;box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);margin:1px auto;max-width:540px;min-width:326px;padding:0;width:calc(100% - 2px);">'
                f'<a href="{post}" target="_blank" rel="noopener">{post}</a></blockquote>\n'
                '<script async src="https://www.instagram.com/embed.js"></script>')


def x_embed(lang="ja"):
    return html(f'<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{NAGARA_X}">{NAGARA_X}</a></blockquote>\n'
                '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


JP_REL = [
    ("https://chomoand-1.com/wiki-liu-kaichi-1041", "リュウ・カイチのwiki風経歴(クラシックの全国大会で入選)"),
    ("https://chomoand-1.com/kaichi-no-manabi-1049", "リュウ・カイチの学歴(名古屋芸術大学で音楽を専攻)"),
    ("https://chomoand-1.com/liu-kaichi-jxc-1198", "リュウ・カイチの両親・家族構成"),
    ("https://chomoand-1.com/rickey-kaichi-instalive-10583", "チェン・リッキーとカイチ先生のインスタライブ"),
    ("https://chomoand-1.com/kaimu-uno-sony-music-artists-14519", "宇野海夢の事務所はソニー(日プ新世界の元練習生)"),
    ("https://chomoand-1.com/producejapan101_datsurakusha-7486", "【日プ新世界】脱落者一覧・全順位結果まとめ"),
]
KR_REL = [
    ("https://chomoand-1.com/ko/kaimu-uno-sony-music-artists-kr-14521", "우노 카이무, 소니 뮤직 아티스츠 소속! 탈락 후 근황은?"),
    ("https://chomoand-1.com/ko/rickey-kaichi-instalive-kr-10595", "첸 리키 & 카이치 인스타 라이브"),
]
EN_REL = [
    ("https://chomoand-1.com/en/kaimu-uno-sony-music-artists-en-14522", "Kaimu Uno signs with Sony Music Artists"),
    ("https://chomoand-1.com/en/rickey-kaichi-instalive-en-12618", "Chen Rickey and Kaichi's Instagram Live"),
]

# ============================== JP ==============================
JP_TITLE = "【日プ新世界】髙城暖人とカイチの事務所は長良！FCはいくら？"
JP_SLUG = "haruto-takagi-liu-kaichi-nagara"

JP_CONTENT = "\n\n".join([
    p("『PRODUCE 101 JAPAN 新世界(日プ新世界・日プ4)』に出演していた髙城暖人(たかぎ・はると)さんとリュウ・カイチさんの所属事務所が決まりました。<br>\n"
      f"2026年10月15日、{mark('2人がそろって長良グループに所属したこと', True)}が、長良プロダクションの公式サイトで発表されています。<br>\n"
      "同じ日には、長良グループの若手俳優・アーティストによる公式ファンクラブ「NAGARA SPARKLE CLUB」もオープンし、2人もメンバーに名を連ねました。<br>\n"
      "翌16日には、カイチさん本人もInstagramで報告し、アイドルという仕事への正直な気持ちをつづっています。<br>\n"
      "この記事では、長良グループがどんな事務所なのか、2人のプロフィールと日プでの歩み、ファンクラブの料金や入会方法をまとめます。"),
    infobox("髙城暖人さん・リュウ・カイチさんの所属の基本情報", [
        ("発表日", "2026年10月15日"),
        ("所属先", "長良グループ(公式プロフィールの所属は「長良マネジメント」)"),
        ("発表した場所", "長良プロダクション公式サイト、2人それぞれのInstagram(髙城さん10月15日・カイチさん10月16日)"),
        ("ファンクラブ", "NAGARA SPARKLE CLUB(10月15日オープン)"),
        ("会費", "月額330円・550円の2コース(税込、入会金なし)"),
        ("日プ新世界での最終順位", "髙城さん70位・カイチさん34位"),
    ]),
    barbox("この記事でわかること", [
        "髙城暖人さんとリュウ・カイチさんの所属事務所",
        "長良グループはどんな事務所？",
        "NAGARA SPARKLE CLUBの料金と特典",
        "2人のプロフィール",
        "カイチさんが本人のInstagramでつづった気持ち",
        "日プ新世界での成績と2人の意外な接点",
    ]),

    h2("髙城暖人とリュウ・カイチの所属事務所はどこ？"),
    minibox([("所属：", "長良グループ(長良マネジメント)"), ("発表：", "2026年10月15日、長良プロダクション公式サイト")]),
    p("10月15日の午前中、長良プロダクションの公式サイトに、髙城さんとカイチさんの2人のプロフィールページが同時に追加されました。<br>\n"
      f"どちらのページにも{mark('所属「長良マネジメント」')}と書かれており、生年月日や身長、趣味・特技とあわせて、本人のInstagramへのリンクも載っています。"),
    p("髙城さんは同じ日のお昼に、自身のInstagramで「この度、長良プロダクションに所属することになりました」と報告しました。<br>\n"
      "長良プロダクションは長良グループの中心となる会社で、公式サイトに書かれている「長良マネジメント」もグループの会社です。<br>\n"
      "2人とも本人の報告では「長良プロダクション」と書いていて、公式サイトの表記とは少し違いますが、どちらも長良グループへの所属を指していると考えてよさそうです。"),
    ig_embed(),
    p("投稿では「オーディションを通して、たくさんの方と出会い、温かい応援をいただけたことは、僕にとってかけがえのないものです」と、日プ新世界のころから応援してくれたファンへの感謝をつづっています。<br>\n"
      "「いつか直接お会いして、感謝の気持ちを伝えられる日を楽しみにしています」という言葉もあり、ファンと会える場をつくりたいという気持ちが伝わってきます。"),
    h3("カイチも10月16日に本人のInstagramで報告"),
    p("カイチさんは、発表の当日には本人のInstagramやXで何も発信していませんでした。<br>\n"
      f"そして翌日の{mark('10月16日の午前10時半ごろ、本人のInstagramに「ご報告」の投稿')}が上がりました。<br>\n"
      "Instagramの更新は6月13日以来で、ファンクラブのアカウント(nagara.sparkleclub)との共同投稿になっています。"),
    ig_embed(KAICHI_IG_POST),
    p("投稿では「この度私は長良プロダクション様と契約させていただくことになりました」と所属を報告しています。<br>\n"
      "目を引くのは、そのあとに続く飾らない言葉です。<br>\n"
      f"日プという大きな挑戦を終えたあと、{mark('アイドルという仕事に対して燃え尽きたような気持ちになり、少し気持ちが離れていた')}と打ち明けました。<br>\n"
      "今も、あのころと同じ気持ちで芸能界に挑めるかは正直わからない、とまで書いています。"),
    p("それでも、長良プロダクションの熱意に触れて「もう一度頑張ってみてもいいかな」と思えたそうです。<br>\n"
      "少しずつあのころの気持ちを取り戻し、心の底からアイドルという職業を選んでよかったと思えるように頑張りたい、と前を向いた言葉で締めくくっています。<br>\n"
      "「皆さんに嘘をつきたくない」という理由で、迷いも含めて自分の言葉で伝えたところに、カイチさんらしい誠実さが表れています。"),
    p("日プ新世界のグループバトルでは、リーダーとして「僕たちはアイドルを仕事にしようとしてるわけだから」とメンバーを引っ張っていたカイチさん。<br>\n"
      "その「アイドルという仕事」に、もう一度向き合うと決めたことになります。<br>\n"
      "番組の放送が終わってから約4か月、進路が気になっていたファンにとっては、本人の口から聞けた待ちに待った知らせになりました。"),

    h2("長良グループはどんな事務所？"),
    minibox([("創業：", "1963年(長良じゅんさんが立ち上げた長良事務所が始まり)"), ("得意分野：", "演歌・歌謡曲の歌手、俳優、タレント")]),
    p("長良グループは、1963年に長良じゅんさんが立ち上げた「長良事務所」から始まった、60年以上の歴史を持つ芸能事務所です。<br>\n"
      "演歌・歌謡曲に強い事務所として知られ、2023年には創立60周年の記念ライブも開いています。"),
    p("公式サイトに載っている主な所属タレントは、次のような顔ぶれです。"),
    table(["ジャンル", "主な所属タレント(公式サイトより)"], [
        ["演歌・歌謡曲", "水森かおり、田川寿美、辰巳ゆうと、岩佐美咲、はやぶさ"],
        ["俳優・タレント", "中村玉緒、グッチ裕三、平野綾、財木琢磨"],
        ["若手俳優・アーティスト", "髙城暖人、リュウ・カイチ、田村継、伊勢之佑人、新田見直登、黒木歩夢、鈴木恒守、松永幸士 など"],
    ]),
    p(f"ここ数年は、ベテラン歌手だけでなく{mark('若手の俳優やアーティストにも力を入れている')}のが特徴です。<br>\n"
      "新しい世代のアーティストを探すプロジェクト「nap(nagara artist project)」も立ち上げており、髙城さんとカイチさんの所属もその流れの中にあるとみられます。<br>\n"
      "日プ新世界の元練習生が演歌の名門に入るのは少し意外にも思えますが、俳優とアーティストの両方の道が開かれている環境だといえます。"),

    h2("NAGARA SPARKLE CLUBとは？料金はいくら？"),
    minibox([("オープン：", "2026年10月15日"), ("会費：", "月額330円 / 550円(税込、入会金なし)")]),
    p("2人の所属発表と同じ10月15日、長良グループの若手俳優・アーティストによる公式ファンクラブ「NAGARA SPARKLE CLUB(ナガラ スパークル クラブ)」がオープンしました。<br>\n"
      "長良グループの公式Xでも、お昼すぎにオープンが告知されています。"),
    x_embed(),
    p("ファンクラブの公式サイトによると、会員になると限定のブログや画像・動画が見られるほか、タレントとリアルタイムで交流できる生配信にも参加できます。<br>\n"
      "コースは2種類で、内容の違いは次のとおりです。"),
    table(["内容", "レギュラー(ベーシック)会員<br>月額330円", "プレミアム会員<br>月額550円"], [
        ["タレントのブログ", "○", "○"],
        ["チケットの先行受付", "○", "○"],
        ["ライブ配信(不定期)", "○", "○"],
        ["ライブ配信のアーカイブ", "×", "○"],
        ["プライベートチャット(準備中)", "×", "○"],
        ["デジタル会員証", "○", "○(プレミアム限定デザイン)"],
    ]),
    p(f"どちらのコースも{mark('入会金は0円')}で、支払いはクレジットカード、各種キャリア決済、あと払いペイディから選べます。<br>\n"
      "注意したいのは、更新日が入会から30日後ではなく「毎月1日」になっている点です。<br>\n"
      "たとえば月末に入会すると、数日後の1日にもう次の月の会費がかかるので、入会するなら月の初めのほうがお得です。"),
    p("オープン初日には、さっそく髙城さんの「自己紹介✨」ブログが公開されました(レギュラー会員以上が見られます)。<br>\n"
      "ブログの一覧にはカイチさんの名前もあり、これから順番に投稿されていくとみられます。<br>\n"
      f"入会は{a(FC_URL, 'NAGARA SPARKLE CLUBの公式サイト')}から、Bitfan IDを作って申し込みます。"),
    leftbox("NAGARA SPARKLE CLUBのメンバー(公式発表より)",
            '<p style="margin:0;">田村継、伊勢之佑人、新田見直登、髙城暖人、リュウ・カイチ、黒木歩夢、鈴木恒守、松永幸士</p>'),

    h2("髙城暖人のプロフィール"),
    minibox([("出身：", "東京都"), ("年齢：", "22歳(2026年10月時点)"), ("身長：", "176cm")]),
    p("長良プロダクションの公式プロフィールと、日プ新世界のころに公開された情報をまとめると次のとおりです。"),
    infobox("髙城暖人さんのプロフィール", [
        ("名前", "髙城暖人(たかぎ・はると)/Haruto Takagi"),
        ("生年月日", "2003年10月26日"),
        ("年齢", "22歳(2026年10月時点)"),
        ("出身地", "東京都"),
        ("身長", "176cm"),
        ("趣味", "散歩"),
        ("特技", "テニス"),
        ("Instagram", a(HARUTO_IG, "@haruto__1026")),
        ("所属", "長良マネジメント(2026年10月15日発表)"),
    ]),
    p(f"出身地の東京都と特技のテニスは、{mark('今回の公式プロフィールで新しく分かった情報')}です。<br>\n"
      "10月26日には23歳の誕生日を迎えるので、所属して最初の誕生日をファンクラブでどう祝うのかも楽しみなところです。<br>\n"
      "Instagramのアカウント名「haruto__1026」も、誕生日の10月26日からとったものとみられます。"),

    h2("リュウ・カイチのプロフィール"),
    minibox([("出身：", "愛知県"), ("年齢：", "22歳(2026年10月時点)"), ("身長：", "184cm")]),
    p("カイチさんの公式プロフィールは、日プ新世界のころとほぼ同じ内容です。"),
    infobox("リュウ・カイチさんのプロフィール", [
        ("名前", "リュウ・カイチ/Liu Kaichi(中国語表記 劉凱馳)"),
        ("生年月日", "2004年2月13日"),
        ("年齢", "22歳(2026年10月時点)"),
        ("出身地", "愛知県"),
        ("身長", "184cm"),
        ("趣味", "アニメ、楽器"),
        ("特技", "自分の良いところをいっぱい言える所"),
        ("Instagram", a(KAICHI_IG, "@kaichiliu.my_shinsekai_")),
        ("所属", "長良マネジメント(2026年10月15日発表)"),
    ]),
    p(f"184cmの長身は、日プ新世界の練習生101人の中で3番目の高さでした。<br>\n"
      f"名古屋芸術大学で音楽を学び、クラリネットで{mark('日本クラシック音楽コンクールの全国大会に入選')}した経歴もあります。<br>\n"
      "番組では、日本語がまだ得意ではない海外の練習生の通訳を買って出る姿から「カイチ先生」と呼ばれ、放送が終わったあとも台湾出身のチェン・リッキーさんのインスタライブで通訳を務めていました。<br>\n"
      "くわしい経歴は<a href=\"https://chomoand-1.com/wiki-liu-kaichi-1041\">リュウ・カイチのwiki風経歴の記事</a>で紹介しています。"),

    h2("日プ新世界での2人の成績は？"),
    minibox([("髙城暖人：", "70位(第1回順位発表式で脱落)"), ("リュウ・カイチ：", "34位(第3回順位発表式で脱落)")]),
    p("じつは2人とも、日プ新世界には「練習生候補」として登場しました。<br>\n"
      "最初のレベル分けテストでは脱落候補になったものの、視聴者のオンライン投票で練習生に昇格し、そろってFクラスから再スタートしています。<br>\n"
      "髙城さんはM!LKの「イイじゃん」、カイチさんはPSYCHIC FEVERの「Paradise」で候補として審査を受けていました。"),
    h3("グループバトルで「リーダー対決」"),
    p(f"2人の大きな接点が、グループバトルのJO1「Love seeker」です。<br>\n"
      f"このとき{mark('カイチさんは1組、髙城さんは2組のリーダー')}を務め、同じ曲で直接対決しました。"),
    table(["", "1組", "2組"], [
        ["リーダー", "リュウ・カイチ(ボーカル3・12票)", "髙城暖人(ラップ1・14票)"],
        ["主なメンバー", "照井康祐、多比奏聖、大瀬凜和、河邉晟、髙橋空良", "南平達矢、浅香孝太郎、澤井星名、北林天虎、森明育"],
        ["チームの票数", "595票(勝利)", "436票"],
    ]),
    p("結果は1組の勝利で、カイチさんがリーダーとしてチームを引っ張りました。<br>\n"
      "カイチさんは練習中に「僕たちはアイドルを仕事にしようとしてるわけだから」とメンバーを鼓舞する場面もあり、まとめ役としての姿が印象に残っています。<br>\n"
      "当時はライバルだった2人が、番組から約4か月後に同じ事務所に入ったことになります。<br>\n"
      "このとき口にした「アイドルを仕事に」という言葉は、10月16日の本人の報告とも重なります。"),
    h3("その後の2人の歩み"),
    p("髙城さんは第1回順位発表式で70位となり、上位50人に入れず脱落しました。<br>\n"
      "カイチさんは第2回順位発表式を31位で通過し、ポジションバトルでは優里の「ベテルギウス」、コンセプトバトルでは「DREAMER」に参加しました。<br>\n"
      "第3回順位発表式では34位となり、ファイナルに進む22人には入れませんでした。<br>\n"
      "ほかの練習生の順位は<a href=\"https://chomoand-1.com/producejapan101_datsurakusha-7486\">日プ新世界の脱落者一覧</a>で確認できます。"),
    p("日プ新世界の元練習生では、10月10日に宇野海夢さんがSony Music Artistsへの所属を発表しています。<br>\n"
      "番組を終えた練習生たちが、それぞれの新しい場所で活動を始めています(<a href=\"https://chomoand-1.com/kaimu-uno-sony-music-artists-14519\">宇野海夢さんの所属の記事</a>)。"),

    h2("髙城暖人とリュウ・カイチの今後の活動は？"),
    minibox([("決まっている活動：", "ファンクラブのブログ・生配信(2026年10月16日時点)"), ("チェック先：", "長良プロダクション公式サイト、各自のInstagram")]),
    p("2026年10月16日時点では、2人のテレビや舞台などの出演予定はまだ発表されていません。<br>\n"
      "長良グループのファンクラブは「若手俳優・アーティスト」向けとされているので、俳優とアーティストのどちらの道に進むのかも注目です。<br>\n"
      "カイチさんは本人の報告で「アイドル」という言葉をくり返し使っていて、アーティストとしての活動を思い描いていることがうかがえます。"),
    p(f"最新情報は、長良プロダクションの公式サイト({a(HARUTO_PAGE, '髙城暖人')}・{a(KAICHI_PAGE, 'リュウ・カイチ')})のお知らせ欄や、本人のInstagramで発表されるとみられます。<br>\n"
      "ファンクラブの生配信で、2人の口から今後の目標が語られる日も近そうです。"),

    h2("まとめ"),
    summarybox([
        "髙城暖人さんとリュウ・カイチさんは、2026年10月15日に長良グループ(長良マネジメント)への所属が発表された",
        "カイチさんは10月16日に本人のInstagramで報告。アイドルの仕事に燃え尽きかけていたが、長良の熱意でもう一度頑張ると決めた",
        "長良グループは1963年創業の老舗で、水森かおりさんや辰巳ゆうとさんなどが所属している",
        "同じ日に公式ファンクラブ「NAGARA SPARKLE CLUB」がオープン。月額330円と550円の2コースで、入会金なし",
        "髙城さんは東京都出身の22歳、カイチさんは愛知県出身の22歳。日プではグループバトル「Love seeker」でリーダー同士として対決した",
        "テレビや舞台などの活動予定はまだ発表されていない",
    ]),
    p("練習生候補から投票で這い上がり、グループバトルでは対決した2人が、同じ事務所で新しいスタートを切りました。<br>\n"
      "迷いも正直に打ち明けたカイチさんが、もう一度アイドルを楽しめる日が来るのを待ちたいですね。<br>\n"
      "番組のころから応援していた方も、これから知ったという方も、2人のこれからをぜひ一緒に見守っていきましょう！"),
    linkbox("髙城暖人・リュウ・カイチ・日プ新世界の関連記事", JP_REL),
])

JP_SUMMARY = ("日プ新世界に出演した髙城暖人さんとリュウ・カイチさんが長良グループに所属。"
              "同じ日にオープンしたファンクラブ「NAGARA SPARKLE CLUB」の料金や、2人のプロフィール、日プでの意外な接点をまとめました。")

# ============================== KR ==============================
KR_TITLE = "[닛프 신세계] 타카기 하루토 & 류 카이치, 나가라 소속! 팬클럽 가격은?"
KR_SLUG = f"{JP_SLUG}-kr"

KR_CONTENT = "\n\n".join([
    p("『PRODUCE 101 JAPAN 新世界(닛프 신세계・닛프4)』에 출연했던 타카기 하루토(髙城暖人)와 류 카이치의 소속사가 정해졌습니다.<br>\n"
      f"2026년 10월 15일, 나가라 프로덕션 공식 사이트를 통해 {mark('두 사람이 함께 나가라 그룹에 소속되었다', True)}는 사실이 공개되었습니다.<br>\n"
      "같은 날 나가라 그룹의 젊은 배우・아티스트들로 구성된 공식 팬클럽 'NAGARA SPARKLE CLUB'도 오픈했으며, 두 사람도 멤버로 이름을 올렸습니다."),
    infobox("소속 발표 기본 정보", [
        ("발표일", "2026년 10월 15일"),
        ("소속", "나가라 그룹(공식 프로필 표기는 '나가라 매니지먼트')"),
        ("발표 채널", "나가라 프로덕션 공식 사이트, 두 사람 각자의 Instagram(하루토 10월 15일・카이치 10월 16일)"),
        ("팬클럽", "NAGARA SPARKLE CLUB(10월 15일 오픈)"),
        ("회비", "월 330엔・550엔 2개 코스(세금 포함, 입회비 없음)"),
        ("닛프 신세계 최종 순위", "타카기 70위・카이치 34위"),
    ]),
    h2("두 사람의 소속사는 어디?"),
    minibox([("소속: ", "나가라 그룹(나가라 매니지먼트)"), ("발표: ", "2026년 10월 15일, 나가라 프로덕션 공식 사이트")]),
    p("10월 15일 오전, 나가라 프로덕션 공식 사이트에 두 사람의 프로필 페이지가 동시에 추가되었습니다.<br>\n"
      "타카기 하루토는 같은 날 낮 Instagram에 '나가라 프로덕션에 소속하게 되었습니다'라고 직접 알렸습니다."),
    ig_embed(),
    p("그는 '오디션을 통해 많은 분들을 만나고 따뜻한 응원을 받은 것은 저에게 둘도 없는 소중한 것'이라며 팬들에게 감사 인사를 전했습니다.<br>\n"
      "류 카이치는 발표 당일에는 본인 SNS에 아무것도 올리지 않았습니다."),
    h3("카이치도 10월 16일 Instagram으로 직접 보고"),
    p(f"다음 날인 {mark('10월 16일 오전 10시 반쯤, 카이치가 Instagram에 보고 게시물')}을 올렸습니다.<br>\n"
      "6월 13일 이후 첫 업데이트로, 팬클럽 계정(nagara.sparkleclub)과의 공동 게시물입니다."),
    ig_embed(KAICHI_IG_POST),
    p("그는 '나가라 프로덕션과 계약하게 되었다'고 알리면서, 큰 도전을 마친 뒤 아이돌이라는 직업에 대해 다 타버린 듯한 기분이 들어 마음이 조금 멀어져 있었다고 솔직하게 털어놓았습니다.<br>\n"
      "그럼에도 나가라 측의 열의 덕분에 '한 번 더 해봐도 좋겠다'고 생각하게 되었고, 그때의 마음을 조금씩 되찾아 아이돌을 선택하길 잘했다고 진심으로 느낄 수 있도록 노력하겠다고 전했습니다.<br>\n"
      "'여러분에게 거짓말을 하고 싶지 않다'며 망설임까지 그대로 전한 점에서 카이치다운 진솔함이 느껴집니다."),
    h2("나가라 그룹은 어떤 회사?"),
    minibox([("창업: ", "1963년(나가라 준이 세운 나가라 사무소에서 시작)"), ("강점: ", "엔카・가요 가수, 배우, 탤런트")]),
    p("나가라 그룹은 60년 넘는 역사를 가진 일본의 연예 기획사로, 엔카・가요에 강한 회사로 알려져 있습니다.<br>\n"
      "미즈모리 카오리, 타츠미 유토, 이와사 미사키, 나카무라 타마오, 히라노 아야 등이 소속되어 있으며, 최근에는 젊은 배우・아티스트 육성에도 힘을 쏟고 있습니다."),
    h2("NAGARA SPARKLE CLUB 가격은?"),
    minibox([("오픈: ", "2026년 10월 15일"), ("회비: ", "월 330엔 / 550엔(세금 포함, 입회비 없음)")]),
    x_embed("ko"),
    table(["내용", "레귤러(베이직) 월 330엔", "프리미엄 월 550엔"], [
        ["탤런트 블로그", "○", "○"],
        ["티켓 선행 접수", "○", "○"],
        ["라이브 방송(비정기)", "○", "○"],
        ["라이브 방송 아카이브", "×", "○"],
        ["프라이빗 채팅(준비 중)", "×", "○"],
        ["디지털 회원증", "○", "○(프리미엄 한정 디자인)"],
    ]),
    p(f"{mark('입회비는 없으며')}, 결제는 신용카드・일본 통신사 결제・Paidy를 이용할 수 있습니다.<br>\n"
      "갱신일은 가입 30일 후가 아니라 '매월 1일'이므로 월초에 가입하는 것이 유리합니다.<br>\n"
      f"오픈 첫날에는 타카기 하루토의 자기소개 블로그가 올라왔습니다. 가입은 {a(FC_URL, '공식 사이트')}에서 Bitfan ID로 할 수 있습니다."),
    h2("타카기 하루토 프로필"),
    minibox([("출신: ", "일본 도쿄도"), ("나이: ", "22세(2026년 10월 기준)"), ("키: ", "176cm")]),
    infobox("타카기 하루토 프로필", [
        ("이름", "타카기 하루토(髙城暖人)/Haruto Takagi"),
        ("생년월일", "2003년 10월 26일"),
        ("출신지", "일본 도쿄도"),
        ("키", "176cm"),
        ("취미", "산책"),
        ("특기", "테니스"),
        ("Instagram", a(HARUTO_IG, "@haruto__1026")),
    ]),
    p("출신지와 특기 테니스는 이번 공식 프로필에서 새롭게 알려진 정보입니다. 10월 26일에는 23세 생일을 맞이합니다."),
    h2("류 카이치 프로필"),
    minibox([("출신: ", "일본 아이치현"), ("나이: ", "22세(2026년 10월 기준)"), ("키: ", "184cm")]),
    infobox("류 카이치 프로필", [
        ("이름", "류 카이치(劉凱馳)/Liu Kaichi"),
        ("생년월일", "2004년 2월 13일"),
        ("출신지", "일본 아이치현"),
        ("키", "184cm"),
        ("취미", "애니메이션, 악기"),
        ("특기", "자신의 좋은 점을 많이 말할 수 있는 것"),
        ("Instagram", a(KAICHI_IG, "@kaichiliu.my_shinsekai_")),
    ]),
    p("나고야예술대학에서 음악을 공부했으며, 클라리넷으로 일본 클래식 음악 콩쿠르 전국대회에 입선한 경력이 있습니다.<br>\n"
      "프로그램에서는 외국인 연습생의 통역을 도맡아 '카이치 선생님'으로 불렸고, 종영 후에도 첸 리키의 인스타 라이브에서 통역을 맡았습니다."),
    h2("닛프 신세계 성적과 두 사람의 접점"),
    minibox([("타카기 하루토: ", "70위(1차 순위 발표식 탈락)"), ("류 카이치: ", "34위(3차 순위 발표식 탈락)")]),
    p("두 사람 모두 '연습생 후보'로 등장해 레벨 테스트에서 탈락 후보가 되었지만, 시청자 온라인 투표로 F클래스에 합류했습니다.<br>\n"
      f"그룹 배틀 JO1 'Love seeker'에서는 {mark('카이치가 1조, 하루토가 2조 리더')}를 맡아 맞대결을 펼쳤고, 1조가 595표 대 436표로 승리했습니다."),
    p("하루토는 1차 순위 발표식에서 70위로 탈락했고, 카이치는 2차를 31위로 통과한 뒤 포지션 배틀 '베텔기우스', 콘셉트 배틀 'DREAMER'를 거쳐 3차 순위 발표식에서 34위로 탈락했습니다.<br>\n"
      "당시 라이벌이었던 두 사람이 약 4개월 만에 같은 회사에 들어간 셈입니다."),
    h2("정리"),
    summarybox([
        "타카기 하루토와 류 카이치는 2026년 10월 15일 나가라 그룹 소속이 발표되었다",
        "카이치는 10월 16일 Instagram으로 직접 보고. 아이돌에 지쳐 있었지만 나가라의 열의로 다시 도전하기로 했다",
        "같은 날 공식 팬클럽 'NAGARA SPARKLE CLUB'이 오픈. 월 330엔・550엔, 입회비 없음",
        "닛프에서는 그룹 배틀 'Love seeker'에서 리더끼리 맞대결했다",
        "TV・무대 등 활동 일정은 아직 발표되지 않았다",
    ]),
    p("같은 회사에서 새 출발을 하는 두 사람을 함께 응원해요!"),
    linkbox("관련 글", KR_REL),
])

KR_SUMMARY = ("닛프 신세계 출신 타카기 하루토와 류 카이치가 나가라 그룹에 소속되었습니다. "
              "같은 날 오픈한 팬클럽 'NAGARA SPARKLE CLUB'의 가격과 두 사람의 프로필, 닛프에서의 접점을 정리했습니다.")

# ============================== EN ==============================
EN_TITLE = "Haruto Takagi & Liu Kaichi Join Nagara Group! How Much Is the New Fan Club?"
EN_SLUG = f"{JP_SLUG}-en"

EN_CONTENT = "\n\n".join([
    p("Haruto Takagi (髙城暖人) and Liu Kaichi, who both appeared on PRODUCE 101 JAPAN SHINSEKAI, have found their new home.<br>\n"
      f"On October 15, 2026, Nagara Production's official website announced that {mark('the two have joined Nagara Group', True)}.<br>\n"
      "On the same day, Nagara Group opened \"NAGARA SPARKLE CLUB,\" an official fan club for its young actors and artists, with both of them as members."),
    infobox("Announcement at a glance", [
        ("Date", "October 15, 2026"),
        ("Agency", "Nagara Group (listed as \"Nagara Management\" on their profiles)"),
        ("Where", "Nagara Production's website and both members' Instagram (Haruto on Oct 15, Kaichi on Oct 16)"),
        ("Fan club", "NAGARA SPARKLE CLUB (opened October 15)"),
        ("Fee", "330 or 550 yen per month (tax incl., no joining fee)"),
        ("Final rank on the show", "Haruto 70th, Kaichi 34th"),
    ]),
    h2("Which agency did they join?"),
    minibox([("Agency: ", "Nagara Group (Nagara Management)"), ("Announced: ", "Oct 15, 2026 on Nagara Production's website")]),
    p("Profile pages for both of them were added to Nagara Production's website on the morning of October 15.<br>\n"
      "Around noon, Haruto shared the news himself on Instagram: \"I have joined Nagara Production.\""),
    ig_embed(),
    p("He thanked his fans, saying that meeting so many people and receiving warm support through the audition meant the world to him.<br>\n"
      "Kaichi stayed quiet on social media on the day of the announcement."),
    h3("Kaichi shares his own announcement on October 16"),
    p(f"The next day, {mark('around 10:30 a.m. on October 16, Kaichi posted an announcement on Instagram')}.<br>\n"
      "It was his first Instagram post since June 13, shared as a collab post with the fan club account (nagara.sparkleclub)."),
    ig_embed(KAICHI_IG_POST),
    p("He confirmed that he has signed with Nagara Production, then opened up about how he really felt.<br>\n"
      "After finishing such a big challenge, he said he had felt burnt out on being an idol and had drifted away from it a little, and that he honestly is not sure he can take on the industry with the same feelings as before.<br>\n"
      "Even so, Nagara's enthusiasm made him think he could give it another try, and he wants to slowly win back those feelings so he can truly say he is glad he chose to be an idol.<br>\n"
      "He wrote that he did not want to lie to his fans, and sharing his doubts so openly feels very much like Kaichi."),
    h2("What is Nagara Group?"),
    minibox([("Founded: ", "1963 (as Nagara Office by Jun Nagara)"), ("Known for: ", "Enka and kayokyoku singers, actors and TV personalities")]),
    p("Nagara Group is a Japanese entertainment agency with more than 60 years of history, best known for enka and kayokyoku singers.<br>\n"
      "Its roster includes Kaori Mizumori, Yuto Tatsumi, Misaki Iwasa, Tamao Nakamura and Aya Hirano, and in recent years it has been building up a lineup of young actors and artists."),
    h2("How much is NAGARA SPARKLE CLUB?"),
    minibox([("Opened: ", "October 15, 2026"), ("Fee: ", "330 / 550 yen per month (tax incl., no joining fee)")]),
    x_embed("en"),
    table(["Content", "Regular (Basic)<br>330 yen/month", "Premium<br>550 yen/month"], [
        ["Talent blogs", "Yes", "Yes"],
        ["Ticket presales", "Yes", "Yes"],
        ["Live streams (irregular)", "Yes", "Yes"],
        ["Live stream archives", "No", "Yes"],
        ["Private chat (coming soon)", "No", "Yes"],
        ["Digital membership card", "Yes", "Yes (Premium design)"],
    ]),
    p(f"There is {mark('no joining fee')}, and you can pay by credit card, Japanese carrier billing or Paidy.<br>\n"
      "Memberships renew on the 1st of every month rather than 30 days after joining, so it's best to sign up early in the month.<br>\n"
      f"Haruto posted a self-introduction blog on opening day. You can join on the {a(FC_URL, 'official site')} with a Bitfan ID."),
    h2("Haruto Takagi's profile"),
    minibox([("From: ", "Tokyo, Japan"), ("Age: ", "22 (as of October 2026)"), ("Height: ", "176cm")]),
    infobox("Haruto Takagi profile", [
        ("Name", "Haruto Takagi (髙城暖人)"),
        ("Birthday", "October 26, 2003"),
        ("Hometown", "Tokyo, Japan"),
        ("Height", "176cm"),
        ("Hobby", "Taking walks"),
        ("Skill", "Tennis"),
        ("Instagram", a(HARUTO_IG, "@haruto__1026")),
    ]),
    p("His hometown and his tennis skills were revealed for the first time on this official profile. He turns 23 on October 26."),
    h2("Liu Kaichi's profile"),
    minibox([("From: ", "Aichi Prefecture, Japan"), ("Age: ", "22 (as of October 2026)"), ("Height: ", "184cm")]),
    infobox("Liu Kaichi profile", [
        ("Name", "Liu Kaichi (劉凱馳)"),
        ("Birthday", "February 13, 2004"),
        ("Hometown", "Aichi Prefecture, Japan"),
        ("Height", "184cm"),
        ("Hobbies", "Anime, musical instruments"),
        ("Skill", "Listing lots of his own good points"),
        ("Instagram", a(KAICHI_IG, "@kaichiliu.my_shinsekai_")),
    ]),
    p("He studied music at Nagoya University of Arts and was selected at the national round of the Japan Classical Music Competition on clarinet.<br>\n"
      "On the show he often interpreted for trainees from overseas, earning the nickname \"Kaichi-sensei,\" and he still interpreted for Chen Rickey on Instagram Live after the show ended."),
    h2("Their results on the show, and a surprising link"),
    minibox([("Haruto Takagi: ", "70th (eliminated at the 1st ranking ceremony)"), ("Liu Kaichi: ", "34th (eliminated at the 3rd ranking ceremony)")]),
    p("Both started as \"trainee candidates\" who were up for elimination in the level test, then made it into Class F through the online viewer vote.<br>\n"
      f"In the group battle for JO1's \"Love seeker,\" {mark('Kaichi led Team 1 and Haruto led Team 2')}, and Team 1 won 595 votes to 436."),
    p("Haruto was eliminated at 70th at the first ranking ceremony. Kaichi passed the second ceremony at 31st, performed \"Betelgeuse\" in the position battle and \"DREAMER\" in the concept battle, and was eliminated at 34th at the third ceremony.<br>\n"
      "Former rivals, the two have now joined the same agency about four months after the show ended."),
    h2("Summary"),
    summarybox([
        "Haruto Takagi and Liu Kaichi joined Nagara Group (announced Oct 15, 2026)",
        "Kaichi shared his own announcement on Instagram on Oct 16, admitting he had felt burnt out but decided to try again",
        "The official fan club NAGARA SPARKLE CLUB opened the same day, at 330 or 550 yen per month with no joining fee",
        "On the show, they faced off as leaders in the \"Love seeker\" group battle",
        "No TV or stage appearances have been announced yet",
    ]),
    p("Let's cheer them on as they start their new chapter at the same agency!"),
    linkbox("Related articles", EN_REL),
])

EN_SUMMARY = ("Former PRODUCE 101 JAPAN SHINSEKAI trainees Haruto Takagi and Liu Kaichi have joined Nagara Group. "
              "Here's the fee for the new fan club NAGARA SPARKLE CLUB, their profiles and their link on the show.")

if __name__ == "__main__":
    if "--update" in sys.argv:
        # 公開済み記事のリライト: タイトル・スラッグ・ステータスは送らず本文だけ更新
        import requests
        env = {}
        for line in open(ROOT / ".env", encoding="utf-8"):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k] = v.strip().strip('"').strip("'")
        auth = (env["WP_KOIKEYS_USERNAME"], env["WP_KOIKEYS_APP_PASSWORD"])
        for pid, c in [(14815, JP_CONTENT), (14817, KR_CONTENT), (14818, EN_CONTENT)]:
            r = requests.post(f"{env['WP_KOIKEYS_URL']}/wp-json/wp/v2/posts/{pid}", auth=auth, json={"content": c})
            r.raise_for_status()
            print("UPDATED", pid, r.json()["status"], r.json()["modified"])
        sys.exit()

    if "--dry" in sys.argv:
        import re
        for name, c in [("JP", JP_CONTENT), ("KR", KR_CONTENT), ("EN", EN_CONTENT)]:
            t = re.sub(r"<!--.*?-->|<script.*?</script>|<[^>]+>", "", c, flags=re.S)
            print(name, "chars:", len(re.sub(r"\s", "", t)))
        print("JP title len", len(JP_TITLE))
        sys.exit()

    JP_EYECATCH_ID = make_eyecatch(
        ["--top", "PRODUCE 101 新世界", "--main", "髙城暖人 & カイチ", "--bottom", "長良グループに所属！", "--bottom", "FCはいくら？"],
        ROOT / "images" / "takagi_kaichi_nagara_1015_eyecatch.png")
    print("JP_EYECATCH_ID", JP_EYECATCH_ID)
    jp = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, "ja", [4, 62], JP_EYECATCH_ID, JP_SUMMARY)
    print("JP_POST_ID", jp["id"], jp["slug"])

    KR_EYECATCH_ID = make_eyecatch(
        ["--top", "PRODUCE 101 新世界", "--main", "하루토 & 카이치", "--bottom", "나가라 그룹 소속!", "--bottom", "팬클럽 가격은?", "--lang", "kr"],
        ROOT / "images" / "takagi_kaichi_nagara_1015_eyecatch_kr.png")
    kr = post_draft(KR_TITLE, KR_CONTENT, KR_SLUG, "ko", [72, 70], KR_EYECATCH_ID, KR_SUMMARY)
    print("KR_POST_ID", kr["id"], kr["slug"])

    en = post_draft(EN_TITLE, EN_CONTENT, EN_SLUG, "en", [116, 112], JP_EYECATCH_ID, EN_SUMMARY)
    print("EN_POST_ID", en["id"], en["slug"])
