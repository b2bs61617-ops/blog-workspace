import urllib.request, urllib.parse, re, html, sys, json, time
names = sys.argv[1:]
out = {}
for n in names:
  for g in ["", "&ggm_group_id=84"]:
    u = "https://bangumi.org/fetch_search_content/?q="+urllib.parse.quote(n)+"&type=tv"+g
    s = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"})).read().decode()
    for b in re.findall(r'<li class="block".*?</li>', s, re.S):
        ps = re.findall(r'<p class="repletion">(.*?)</p>', b, re.S)
        eid = re.search(r'ebisId&quot;:&quot;(.*?)&quot;', b)
        if len(ps)>=2:
            key=(ps[1].strip(), html.unescape(ps[0]).strip())
            out.setdefault(key, set()).add(n + ("(関西)" if g else ""))
            out[key].add("id="+(eid.group(1) if eid else ""))
    time.sleep(0.3)
def k(x):
    m=re.match(r"(\d+)月(\d+)日.*?(\d+):(\d+)",x[0]); return tuple(map(int,m.groups())) if m else (99,)
for key in sorted(out,key=k):
    print(key[0],"|",key[1],"|",",".join(sorted(out[key])))
