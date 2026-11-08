import urllib.request, re, html, sys
for eid in sys.argv[1:]:
    s = urllib.request.urlopen(urllib.request.Request("https://bangumi.org/tv_events/"+eid, headers={"User-Agent":"Mozilla/5.0"})).read().decode()
    i = s.find('class="program_title'); j = s.find('talent_click', i)
    t = s[i:j] if i>0 else ""
    t = html.unescape(re.sub(r"<[^>]+>","\n",t))
    t = "\n".join(l.strip() for l in t.splitlines() if l.strip())
    names = sorted(set(re.findall(r'talent_click.*?&quot;name&quot;:&quot;(.*?)&quot;', s)))
    print("=====",eid); print(t[:2500]); print("出演:", "、".join(names)[:600])
