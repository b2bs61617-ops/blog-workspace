import sys
import re
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

def extract_video_id(url):
    patterns = [
        r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(url_or_id):
    video_id = extract_video_id(url_or_id) or url_or_id

    api = YouTubeTranscriptApi()

    try:
        transcript = api.fetch(video_id, languages=['ja'])
    except NoTranscriptFound:
        try:
            transcript = api.fetch(video_id, languages=['en'])
        except NoTranscriptFound:
            transcript_list = api.list(video_id)
            first = next(iter(transcript_list))
            transcript = first.fetch()

    full_text = ' '.join(entry.text for entry in transcript)
    return full_text

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('使い方: python youtube_transcript.py <YouTubeのURLまたは動画ID>')
        sys.exit(1)

    url = sys.argv[1]
    text = get_transcript(url)
    print(text)
