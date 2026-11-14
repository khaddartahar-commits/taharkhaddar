import requests, concurrent.futures, os

# الملفات اللي نفحصوهم - غير العربي
FILES = ["arabic-maghreb.m3u", "arabic-mashreq.m3u"]

def is_working(url):
    try:
        # نفحص غير الراس، ما نحملوش الفيديو - اقتصادي
        r = requests.head(url, timeout=5, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code in [200, 301, 302, 403]:
            return True
        # كاش سيرفرات ما تقبلش HEAD، نجربو GET صغير
        r = requests.get(url, timeout=5, stream=True, headers={"User-Agent": "Mozilla/5.0"})
        return r.status_code in [200, 301, 302, 403]
    except:
        return False

def parse_m3u(path):
    if not os.path.exists(path):
        print(f"ماكاش {path} - نتخطاوه")
        return []
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()
    chans = []
    ext = ""
    for line in lines:
        line=line.strip()
        if line.startswith("#EXTINF"):
            ext=line
        elif line.startswith("http") and ext:
            chans.append((ext, line))
            ext=""
    return chans

for fname in FILES:
    chans = parse_m3u(fname)
    print(f"🔍 {fname}: {len(chans)} قناة - نفحصو...")
    if not chans:
        continue
    # نفحصو 30 قناة في نفس الوقت - سريع
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
        results = list(ex.map(lambda c: is_working(c[1]), chans))
    working = [c for c, ok in zip(chans, results) if ok]
    print(f"✅ {fname}: {len(working)} / {len(chans)} شغالة")
    with open(fname, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ext, url in working:
            f.write(ext + "\n" + url + "\n")
    print(f"💾 حفظنا {fname}")

print("🎉 كملنا الفحص")
