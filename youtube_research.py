#!/usr/bin/env python3
"""
YouTube調査ツール - トレンド人物の公式チャンネルを自動調査してAIで分析

使い方:
  python youtube_research.py 花田藍衣
  python youtube_research.py 花田藍衣 --max 20
"""

import sys
import io
import json
import subprocess
import re
import argparse
import os
from datetime import datetime

# Windows PowerShell文字化け対策
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import anthropic

# ========== YouTube検索・チャンネル取得 ==========

def run_yt_dlp(args):
    """yt-dlpを実行してstdoutを返す"""
    env = os.environ.copy()
    cmd = [sys.executable, '-m', 'yt_dlp'] + args + ['--no-warnings']
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', env=env)
    return result.stdout, result.stderr

def search_official_channel(keyword):
    """キーワードで公式チャンネルを検索して特定する"""
    print(f"\n[STEP 1] '{keyword}' の公式チャンネルを検索中...")

    search_queries = [
        f"{keyword} 公式",
        f"{keyword} official",
        keyword,
    ]

    for query in search_queries:
        stdout, _ = run_yt_dlp([
            f'ytsearch20:{query}',
            '--dump-json',
            '--flat-playlist',
        ])

        channels_found = {}
        for line in stdout.strip().split('\n'):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            uploader = data.get('uploader') or data.get('channel') or ''
            channel_url = data.get('channel_url') or data.get('uploader_url') or ''
            channel_id = data.get('channel_id') or data.get('uploader_id') or ''

            if not uploader or not channel_url:
                continue

            # キーワードの各単語がチャンネル名に含まれているか
            kw_parts = re.split(r'[\s　]+', keyword)
            match_score = sum(1 for p in kw_parts if p and p in uploader)

            if match_score > 0:
                if channel_url not in channels_found or channels_found[channel_url]['score'] < match_score:
                    channels_found[channel_url] = {
                        'name': uploader,
                        'url': channel_url,
                        'score': match_score
                    }

        if channels_found:
            best = sorted(channels_found.values(), key=lambda x: x['score'], reverse=True)[0]
            print(f"  → 公式チャンネル発見: {best['name']}")
            print(f"  → URL: {best['url']}")
            return best['url'], best['name']

    print("  → 公式チャンネルは見つかりませんでした")
    return None, None


def get_channel_videos(channel_url, max_videos=30):
    """チャンネルの動画一覧を取得"""
    print(f"\n[STEP 2] 動画一覧を取得中（最大{max_videos}本）...")

    stdout, _ = run_yt_dlp([
        channel_url,
        '--dump-json',
        '--flat-playlist',
        '--playlist-end', str(max_videos),
    ])

    videos = []
    for line in stdout.strip().split('\n'):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        video_id = data.get('id', '')
        title = data.get('title', '')
        # YouTube動画IDは11文字
        if video_id and len(video_id) == 11 and title:
            videos.append({'id': video_id, 'title': title})

    print(f"  → {len(videos)}本の動画を取得")
    return videos


# ========== 文字起こし取得 ==========

def get_transcript(video_id):
    """動画の文字起こしをテキストで返す（取得できなければNone）"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # 日本語優先、なければ自動生成でも可
        for lang in ['ja', 'ja-JP']:
            try:
                t = transcript_list.find_transcript([lang])
                entries = t.fetch()
                return ' '.join(e['text'] for e in entries)
            except Exception:
                pass

        # 自動生成字幕を試みる
        try:
            t = transcript_list.find_generated_transcript(['ja', 'ja-JP'])
            entries = t.fetch()
            return ' '.join(e['text'] for e in entries)
        except Exception:
            pass

        return None

    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception:
        return None


# ========== AI分析 ==========

def analyze_with_claude(keyword, transcripts_data):
    """Claude Haiku APIで文字起こし内容から個人情報を抽出"""
    print("\n[STEP 4] AIが内容を分析中...")

    # 各動画の文字起こしを結合（1動画あたり最大4000字）
    combined = ""
    for v in transcripts_data:
        if v['transcript']:
            combined += f"\n=== 動画: {v['title']} ===\n"
            combined += v['transcript'][:4000]
            combined += "\n"

    if not combined.strip():
        return "文字起こしを取得できた動画がありませんでした。X・Instagramでの調査に切り替えてください。"

    # 全体が長すぎる場合は切り詰め
    if len(combined) > 60000:
        combined = combined[:60000] + "\n...(文字数制限により省略)"

    client = anthropic.Anthropic()

    prompt = f"""以下は「{keyword}」さんのYouTube動画（複数）の文字起こしです。
ブログ記事のリサーチ用として、動画内の発言から以下の情報を抽出してください。

【抽出項目】
1. 学歴・高校・大学（どこに通っていたか、いつ卒業したか）
2. 家族構成（父・母・兄弟姉妹の有無、職業、エピソード）
3. 出身地・地元・実家（生まれた場所、育った場所、実家のエピソード）
4. 恋愛情報（現在・過去の恋人、熱愛の話題、恋愛観）
5. 趣味・特技（好きなこと、得意なこと、ハマっていること）
6. その他のブログネタになる個人情報・エピソード

【出力ルール】
- 発言があった場合のみ記載する（「〜と発言」「〜と述べた」と根拠を示す）
- 発言がない項目は「発言なし」と記載する
- 複数動画にまたがる場合はまとめて整理する

---文字起こし---
{combined}
"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


# ========== メイン ==========

def main():
    parser = argparse.ArgumentParser(description='YouTube調査ツール')
    parser.add_argument('keyword', help='調査するキーワード（例: 花田藍衣）')
    parser.add_argument('--max', type=int, default=30, help='取得する最大動画数（デフォルト: 30）')
    args = parser.parse_args()

    keyword = args.keyword
    max_videos = args.max

    print("=" * 55)
    print(f"  YouTube調査ツール")
    print(f"  キーワード: {keyword}")
    print(f"  最大動画数: {max_videos}本")
    print("=" * 55)

    # STEP 1: 公式チャンネルを探す
    channel_url, channel_name = search_official_channel(keyword)

    if not channel_url:
        print("\n[結果] 公式チャンネルが見つかりませんでした。")
        print("→ Xiツール（X・Instagram）での調査に切り替えてください。")
        sys.exit(0)

    # STEP 2: 動画一覧を取得
    videos = get_channel_videos(channel_url, max_videos)

    if not videos:
        print("\n[結果] 動画が見つかりませんでした。")
        sys.exit(0)

    # STEP 3: 文字起こし取得
    print(f"\n[STEP 3] 文字起こし取得中...")
    transcripts_data = []
    success = 0

    for i, video in enumerate(videos, 1):
        title_short = video['title'][:45] + ('...' if len(video['title']) > 45 else '')
        print(f"  [{i:2}/{len(videos)}] {title_short}", end=' ')
        transcript = get_transcript(video['id'])
        if transcript:
            print("✓")
            success += 1
        else:
            print("✗ 字幕なし")
        transcripts_data.append({**video, 'transcript': transcript})

    print(f"\n  → {success}/{len(videos)}本の文字起こしを取得しました")

    if success == 0:
        print("\n[結果] 字幕付き動画がありませんでした。")
        sys.exit(0)

    # STEP 4: AI分析
    analysis = analyze_with_claude(keyword, transcripts_data)

    # STEP 5: 結果表示＋ファイル保存
    output = f"""
{"=" * 55}
【{keyword}】YouTube調査結果
調査日時: {datetime.now().strftime("%Y-%m-%d %H:%M")}
チャンネル: {channel_name}
動画数: {len(videos)}本 / 文字起こし成功: {success}本
{"=" * 55}

{analysis}

{"=" * 55}
"""

    print(output)

    # ファイルにも保存
    safe_keyword = re.sub(r'[\\/:*?"<>|]', '_', keyword)
    filename = f"youtube_research_{safe_keyword}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"[保存] {filename}")


if __name__ == "__main__":
    main()
