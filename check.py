import requests

# كل الروابط - يجيب منهم كلش
SOURCES_MAGHREB = [
    "https://iptv-org.github.io/iptv/countries/dz.m3u",
    "https://iptv-org.github.io/iptv/countries/ma.m3u",
    "https://iptv-org.github.io/iptv/countries/tn.m3u",
    "https://iptv-org.github.io/iptv/countries/ly.m3u",
    "https://iptv-org.github.io/iptv/countries/eg.m3u",
    "https://iptv-org.github.io/iptv/countries/mr.m3u",
]
SOURCES_MASHREQ = [
    "https://iptv-org.github.io/iptv/countries/sa.m3u",
    "https://iptv-org.github.io/iptv/countries/ae.m3u",
    "https://iptv-org.github.io/iptv/countries/qa.m3u",
    "https://iptv-org.github.io/iptv/countries/kw.m3u",
    "https://iptv-org.github.io/iptv/countries/iq.m3u",
    "https://iptv-org.github.io/iptv/countries/jo.m3u",
    "https://iptv-org.github.io/iptv/countries/lb.m3u",
    "https://iptv-org.github.io/iptv/countries/sy.m3u",
    "https://iptv-org.github.io/iptv/countries/ye.m3u",
    "https://iptv-org.github.io/iptv/countries/ps.m3u",
]

def fetch(url):
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200 and "#EXTM3U" in r.text:
            return r.text
    except Exception as e:
        print(f"❌ {url} - {e}")
    return ""

def parse(text):
    lines = text.splitlines()
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

def build(sources, out_file):
    all_chans = []
    seen_url = set()
    for s in sources:
        print(f"📥 {s}...")
        t = fetch(s)
        if not t: continue
        for ext, url in parse(t):
            # نحذف غير المكرر بنفس الرابط - الميت نخليوه
            if url not in seen_url:
                seen_url.add(url)
                all_chans.append((ext, url))
    print(f"📦 {out_file} - لقينا {len(all_chans)} قناة - كلش، شغالة و ميتة")
    if len(all_chans) < 5:
        print("⚠️ قليل بزاف، ما نحفظوش")
        return
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ext, url in all_chans:
            f.write(ext + "\n" + url + "\n")
    print(f"✅ حفظنا {out_file} - {len(all_chans)} قناة")

build(SOURCES_MAGHREB, "arabic-maghreb.m3u")
build(SOURCES_MASHREQ, "arabic-mashreq.m3u")
print("🎉 كملنا - جبنا كلش")
