import sys
exec(open(r"C:\Users\s30se\Desktop\blog-workspace\tools\_tv1108_1107\upload.py",encoding="utf-8").read().split("for key,pid")[0])
D=r"C:\Users\s30se\Desktop\blog-workspace\tools\_tv1108_1108"
for key,pid in [("CHOMO4",2348),("CHOMO2",523),("AUDITION",1292),("CHOMO5",582),("KOIKEYS",15407),("KOIKEYS",15408),("KOIKEYS",15409)]:
    p = api(key, f"/wp-json/wp/v2/posts/{pid}?context=edit")
    open(rf"{D}\wp_{pid}.html","w",encoding="utf-8",newline="\n").write(p["content"]["raw"])
    print(pid, p["status"], p["title"]["raw"], p["modified"], len(p["content"]["raw"]))
