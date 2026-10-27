"""chomoand-0.com を SixTONES 専門サイトに作り直す(2026-10-27)。
旧データは同フォルダの posts.json / categories.json / widgets.json / page_26_profile.json / settings.json。"""
import os, sys, json, requests, time
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
def load_dotenv(p):
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if l and not l.startswith("#") and "=" in l:
            k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip("\"'"))
load_dotenv('.env')
SITE = os.environ['WP_AUDITION_URL'].rstrip('/')
U = SITE + '/wp-json'; A = (os.environ['WP_AUDITION_USERNAME'], os.environ['WP_AUDITION_APP_PASSWORD'])
U2 = os.environ['WP_CHOMO2_URL'].rstrip('/') + '/wp-json'; A2 = (os.environ['WP_CHOMO2_USERNAME'], os.environ['WP_CHOMO2_APP_PASSWORD'])
D = 'backups/chomoand0_sixtones_reset_2026-10-27/'
LOG = []
def call(m, p, **k):
    r = requests.request(m, U + p, auth=A, timeout=60, **k)
    LOG.append((m, p, r.status_code)); print(m, p, r.status_code, '' if r.ok else r.text[:200]); return r

MEMBERS = [  # 名前, slug, 色, 色名
    ('ジェシー', 'jesse', '#e53935', '赤'),
    ('京本大我', 'kyomoto-taiga', '#f06292', 'ピンク'),
    ('松村北斗', 'matsumura-hokuto', '#333333', '黒'),
    ('髙地優吾', 'kochi-yugo', '#f9b800', '黄'),
    ('森本慎太郎', 'morimoto-shintaro', '#43a047', '緑'),
    ('田中樹', 'tanaka-juri', '#1e88e5', '青'),
]

# 1. サイト名
call('POST', '/wp/v2/settings', json={'title': 'ちょものSixTONES情報局', 'description': ''})

# 2. プラグイン(エネブロ表で足りない1つ)
call('POST', '/wp/v2/plugins', json={'slug': 'wp-content-copy-protector', 'status': 'active'})

# 3. 記事をすべてゴミ箱へ
for p in json.load(open(D + 'posts.json', encoding='utf-8')):
    call('DELETE', f"/wp/v2/posts/{p['id']}"); time.sleep(0.3)

# 4. カテゴリー: トラジャ系を削除、ジャニーズ(既定カテゴリー id3)は名前そのまま slug を johnnys に、SixTONES+メンバー作成
for c in json.load(open(D + 'categories.json', encoding='utf-8')):
    if c['id'] != 3:
        call('DELETE', f"/wp/v2/categories/{c['id']}", params={'force': True})
call('POST', '/wp/v2/categories/3', json={'slug': 'johnnys'})
g = call('POST', '/wp/v2/categories', json={'name': 'SixTONES', 'slug': 'sixtones'}).json()
cats = {'SixTONES': g['id']}
for name, slug, *_ in MEMBERS:
    cats[name] = call('POST', '/wp/v2/categories', json={'name': name, 'slug': slug, 'parent': g['id']}).json()['id']
json.dump(cats, open(D + 'new_categories.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 5. トップの「メンバーから探す」をSixTONES版に
cards = ''.join(f'''
<a href="{SITE}/category/sixtones/{slug}" style="display:flex;flex-direction:column;align-items:center;text-decoration:none;width:80px;">
  <span style="display:block;width:56px;height:56px;border-radius:50%;background:{col};border:3px solid #e0e0e0;box-shadow:0 2px 6px rgba(0,0,0,0.12);"></span>
  <span style="margin-top:6px;font-size:12px;font-weight:bold;color:#333;line-height:1.3;text-align:center;">{name}</span>
  <span style="font-size:10px;color:{col};">{cname}</span>
</a>
''' for name, slug, col, cname in MEMBERS)
html = f'''<!-- wp:html -->
<div style="background:#f7f7f7;border:1px solid #dddddd;border-radius:12px;padding:20px 16px;margin:0 0 24px;">
  <h2 style="margin:0 0 14px;font-size:1.15em;color:#222;text-align:center;">メンバーから探す</h2>
  <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:14px;">
{cards}
  </div>
</div>
<!-- /wp:html -->'''
call('POST', '/wp/v2/widgets/block-7', json={'instance': {'raw': {'content': html}}})

# 6. プロフィール: chomoand-2 版を SixTONES 向けに移植(写真2枚もアップロード)
def upload(url, fname):
    b = requests.get(url, timeout=60).content
    return call('POST', '/wp/v2/media', data=b, headers={'Content-Disposition': f'attachment; filename={fname}', 'Content-Type': 'image/jpeg'}).json()
src = requests.get(U2 + '/wp/v2/pages/12', auth=A2, params={'context': 'edit'}).json()['content']['raw']
for old, fname in [(31, 'profile-anco.jpg'), (32, 'profile-momo.jpg')]:
    m = upload(f'https://chomoand-2.com/wp-content/uploads/2026/10/{fname}', fname)
    src = src.replace(f'"id":{old}', f'"id":{m["id"]}').replace(f'wp-image-{old}', f'wp-image-{m["id"]}') \
             .replace(f'https://chomoand-2.com/wp-content/uploads/2026/10/{fname}', m['source_url'])
src = src.replace('9人それぞれの個性と、息の合ったパフォーマンスやアクロバットには毎回感動してしまいます。',
                  '6人それぞれの個性と、圧倒的な歌唱力やライブでの迫力、わちゃわちゃしたトークには毎回夢中になってしまいます。')
src = src.replace('Snow Manのパフォーマンスとわちゃわちゃ感', 'SixTONESのパフォーマンスとわちゃわちゃ感')
src = src.replace('Snow Man', 'SixTONES')
src = src.replace('<li><a href="https://chomoand-1.com/">',
                  '<li><a href="https://chomoand-2.com/">ちょものSnow Manブログ</a>（Snow Manの情報をまとめています）</li><li><a href="https://chomoand-1.com/">')
assert 'Snow Man' not in src.replace('ちょものSnow Manブログ', '').replace('Snow Manの情報', ''), 'Snow Man残り'
call('POST', '/wp/v2/pages/26', json={'content': src})

json.dump(LOG, open(D + 'apply_log.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('NG:', [x for x in LOG if x[2] >= 300])
