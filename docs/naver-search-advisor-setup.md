# Naver Search Advisor(네이버 서치어드바이저)のセットアップ手順

**現在の状態(2026-08-02)**: 未セットアップ。chomoand-1.com(コイキーズブログ)の韓国語版記事([docs/korea-expansion.md](korea-expansion.md)参照)がNaverにインデックスされているか未確認で、登録もされていない可能性が高い。

**Why:** [Google Indexing API](google-indexing-setup.md)はGoogle向けのインデックス即時通知には使えるが、韓国最大手の検索エンジンであるNaverには効かない。Naverは独自のクローラーを持ち、Googleと同じSEO対策(サイトマップ・構造化データ等)だけでは拾われにくいことで知られている。韓国語読者への露出を狙うなら、Naver独自の登録が別途必要。

**注意(APIの有無について):** GoogleのIndexing APIのような「URLを送信するだけで即時インデックスをリクエストできる公開API」はNaver Search Advisorには**存在しない**(2026-08-02時点で確認)。サイト所有権確認・サイトマップ提出・個別URLの収集요청(クロール要請)は、いずれもNaver Search Advisorの管理画面上でのマニュアル操作が基本。将来的にPlaywright等でUI操作を自動化する余地はあるが、ログインセッションの扱いが必要になり壊れやすいため、このドキュメントでは手動運用の手順のみ扱う。

## 1. サイト登録・所有権確認(トモキ本人が実施)

1. [Naver Search Advisor](https://searchadvisor.naver.com/)にアクセスし、Naverアカウントでログイン
2. 「サイト管理」→「サイト登録」で`https://chomoand-1.com`を追加
3. 所有権確認方法を選ぶ(いずれか1つ):
   - **HTMLタグ**: 発行されたmetaタグをWordPressテーマの`<head>`に追加(SWELLテーマなら「外観」→「カスタマイズ」→「head内タグ」に貼り付け可能)
   - **HTMLファイルアップロード**: 発行されたファイルをサーバーのルート直下に設置
   - **RSS確認**: サイトのRSSフィードURLを指定
4. 確認が完了するとダッシュボードにサイトが表示される

日本語版(chomoand.com・chomoand-0.com)はNaver向けの露出を狙う対象ではないため登録不要。

## 2. サイトマップ提出(トモキ本人が実施)

1. 登録したサイトのダッシュボード→「要請」→「사이트맵 제출(サイトマップ提出)」
2. `sitemap.xml`(既存の`https://chomoand-1.com/sitemap.xml`をそのまま指定)を提出
3. 日本語記事・韓国語記事の両方が同じsitemapインデックスに含まれているため、追加のsitemap分割は不要

## 3. 個別記事の収集要請(公開のたびに実施、当面は手動)

1. ダッシュボード→「요청」→「웹페이지 수집(ウェブページ収集)」
2. 韓国語記事を公開した直後に、そのURL(`https://chomoand-1.com/ko/記事slug`)を入力して収集要請
3. 1日あたりのリクエスト上限があるため、公開が重なる日は優先度の高い記事から要請する

**将来の自動化案(未実装)**: [publishスキル](../.claude/skills/publish/SKILL.md)でGoogle Indexing APIを呼んでいる箇所と同じタイミングで、Playwrightを使ってNaver Search Advisorにログインし収集要請フォームを自動送信する案はある。ただしログインセッション(Cookie)の保存・失効対応が必要で、`tools/Xiy/`のX収集と同様にUI変更に弱い。優先度が上がった場合はここに追記する。

## 4. 動作確認

Naver検索で`site:chomoand-1.com`を検索し、`/ko/`配下のページがヒットするか確認する。ヒットしない場合は収集要請から反映までに数日〜数週間かかることがあるため、時間を置いて再確認する。

## 使われている場所

現時点ではどこからも自動で呼ばれていない(手動運用のみ)。将来Playwright自動化を実装する場合は、[publishスキル](../.claude/skills/publish/SKILL.md)のGoogle Indexing API呼び出し箇所に追記する形になる見込み。
