# Naverインデックス登録(IndexNowプロトコル)のセットアップ手順

**現在の状態(2026-08-02)**: 未セットアップ。キーは生成済みだが、サイト直下への検証ファイル設置(下記1)がまだ。

**訂正(2026-08-02):** 当初このドキュメントに「Naverには公開APIが無く手動運用しかない」と書いたが誤りだった。Naverは2023年7月から**IndexNowプロトコル**(Bing・Yandex等と共通の公開API規格)に対応しており、GETリクエスト1本でインデックス登録をリクエストできる。Google Indexing APIのようなOAuth/サービスアカウントも不要で、ログイン・ブラウザ操作も一切不要。

**Why:** [Google Indexing API](google-indexing-setup.md)はGoogle向けで、韓国最大手の検索エンジンであるNaverには効かない。コイキーズブログ(chomoand-1.com)の韓国語記事([docs/korea-expansion.md](korea-expansion.md)参照)をNaverの読者に届けるには別途登録が必要。

## 1. キー検証ファイルの設置(トモキ本人が実施・初回のみ)

IndexNowは「このキーを知っている=サイトの所有者」という認証方式で、**サイトのドメイン直下に、キー文字列そのものを中身とするtxtファイルを置くだけ**で完了する。

1. 生成済みのキー: `ff9c46dd9d99fc9060510f013f108d69`(このドキュメント作成時にマツが生成。値自体は秘密情報ではないのでここに書いてよい)
2. 中身が`ff9c46dd9d99fc9060510f013f108d69`の1行だけのテキストファイルを作り、ファイル名を`ff9c46dd9d99fc9060510f013f108d69.txt`にする
3. Xserverのサーバーパネル→ファイルマネージャー(またはFTPクライアント)で、`chomoand-1.com`のドキュメントルート直下(`public_html`等、WordPressの`wp-config.php`があるのと同じ階層)にこのファイルをアップロードする
4. ブラウザで`https://chomoand-1.com/ff9c46dd9d99fc9060510f013f108d69.txt`にアクセスし、キー文字列だけが表示されればOK

**マツ(Claude Code)はXserverの認証情報を持っていないため、この設置作業だけはトモキ本人にお願いする必要がある**([docs/wordpress.md](wordpress.md)のDNS障害対応時と同じ理由)。それ以外(下記2・3)はマツが自動で行う。

## 2. ローカル設定(マツが実施済み)

`.env`に以下を追加済み:
```
NAVER_INDEXNOW_KEY=ff9c46dd9d99fc9060510f013f108d69
```

## 3. 動作確認

1番のファイル設置が終わったら:
```
python tools/naver_indexnow.py https://chomoand-1.com/ko/ko1keyz-leader-daiki-kr-10982
```
HTTPステータス200が返れば受理成功。Naverの検索ロボットが実際にクロールしてインデックスされるまでは別途時間がかかる(即時反映ではない)。

参考: 単一URL用のエンドポイントは`https://searchadvisor.naver.com/indexnow?url={URL}&key={キー}`(GET)。まとめて送りたい場合は`https://api.searchadvisor.naver.com/indexnow`へPOSTし、ボディに`{"host": "chomoand-1.com", "key": "...", "keyLocation": "https://chomoand-1.com/ff9c46dd9d99fc9060510f013f108d69.txt", "urlList": [...]}`を渡す(最大10,000件/回)。

## 使われている場所

- `tools/naver_indexnow.py`: IndexNow呼び出し本体
- [publishスキル](../.claude/skills/publish/SKILL.md): chomoand-1.comの記事を公開した直後、Google Indexing APIの呼び出しに続けて自動実行。`NAVER_INDEXNOW_KEY`未設定の場合は通知だけスキップし、公開処理自体は止まらない(Google Indexing APIと同じフェイルセーフ方式)

## 補足: Naver Search Advisorへのサイト登録自体は別

上記のIndexNowは「個別記事を即座にクロール候補に入れる」ための仕組み。それとは別に、サイト全体の検索パフォーマンス(表示回数・クリック数等の計測)を見たい場合は、従来通り[Naver Search Advisor](https://searchadvisor.naver.com/)でのサイト登録(HTMLタグ確認等)・サイトマップ提出も別途やっておくと良い。ただしインデックス登録のリクエスト自体はIndexNowだけで完結するため、Search Advisor登録は必須ではない。
