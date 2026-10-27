"""4サイトのプロフィール「運営しているサイト」にSixTONES(chomoand-0.com)を追加(2026-10-27)。
旧本文は同フォルダの before_<site>.json。"""
import os, json, requests
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
for l in open('.env', encoding='utf-8'):
    l = l.strip()
    if l and not l.startswith('#') and '=' in l:
        k, v = l.split('=', 1); os.environ.setdefault(k.strip(), v.strip().strip("\"'"))
D = 'backups/profile_sister_sixtones_2026-10-27/'
LI = '<li><a href="https://chomoand-0.com/">ちょものSixTONES情報局</a>（SixTONESの情報をまとめています）</li>'
for pref, pid in [('KOIKEYS', 30), ('CHOMO2', 12), ('CHOMO4', 14), ('CHOMO5', 14)]:
    U = os.environ[f'WP_{pref}_URL'].rstrip('/') + '/wp-json'; A = (os.environ[f'WP_{pref}_USERNAME'], os.environ[f'WP_{pref}_APP_PASSWORD'])
    p = requests.get(f'{U}/wp/v2/pages/{pid}', auth=A, params={'context': 'edit'}, timeout=60).json()
    raw = p['content']['raw']
    json.dump(p, open(D + f'before_{pref}.json', 'w', encoding='utf-8'), ensure_ascii=False)
    if 'chomoand-0.com' in raw:
        print(pref, 'already'); continue
    i = raw.find('<!-- sister-sites -->'); assert i >= 0, pref
    j = raw.find('</ul>', i); assert j >= 0, pref
    new = raw[:j] + LI + raw[j:]
    r = requests.post(f'{U}/wp/v2/pages/{pid}', auth=A, json={'content': new}, timeout=60)
    print(pref, p['title']['raw'], r.status_code)
