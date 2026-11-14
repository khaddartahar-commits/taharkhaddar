# 📦 كل الأكواد في ملف واحد - TAHAR KHADDAR IPTV

---

## 1️⃣ check.py

```python
import requests, re
print("🚀 بدأ الفرز - 3 ملفات + إنترنت")
headers = {'User-Agent': 'Mozilla/5.0'}
def get_lines(url):
    try:
        r = requests.get(url, timeout=30, headers=headers)
        if r.status_code == 200:
            return r.text.splitlines()
    except:
        pass
    return []
def is_radio(inf, url):
    low = (inf + " " + url).lower()
    if 'group-title="radio"' in low or 'tvg-type="radio"' in low:
        return True
    if any(k in low for k in [' fm','fm ','.mp3','radio ','إذاعة','اذاعة','راديو','quran radio','radio quran']):
        if ' tv' not in low and 'tv ' not in low and 'channel' not in low:
            return True
    return False
def add(store, inf, url):
    url = url.strip()
    if not url.startswith('http') or url in store:
        return
    if 'localhost' in url or 'example.com' in url:
        return
    if is_radio(inf, url):
        return
    store[url] = inf.strip()
print("1. القنوات العربية...")
arabic = {}
for code in ['dz','ma','tn','eg','sa','ae','qa','kw','jo','lb','iq','ye','ps','sy','ly','sd','mr','bh','om']:
    lines = get_lines(f'https://iptv-org.github.io/iptv/countries/{code}.m3u')
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
            add(arabic, lines[i], lines[i+1])
lines = get_lines('https://iptv-org.github.io/iptv/languages/ara.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        add(arabic, lines[i], lines[i+1])
lines = get_lines('https://iptv-org.github.io/iptv/regions/mena.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        low = lines[i].lower()
        is_ar = 'language="arabic"' in low or 'ara' in low or any(f'country="{c}"' in low for c in ['dz','ma','tn','eg','sa','ae','qa','kw','jo','lb','iq','ye','ps','sy','ly','sd','mr','bh','om'])
        if not is_ar:
            name = lines[i].split(',')[-1]
            if any('\u0600' <= ch <= '\u06FF' for ch in name):
                is_ar = True
        if is_ar:
            add(arabic, lines[i], lines[i+1])
print(f"✅ 1. عربية: {len(arabic)} - بدون راديو")
print("🌐 نزيدو قنوات الإنترنت فقط...")
internet_only = [
    ("🌐 الجديد - Al Jadeed [Internet]", "https://livestreaming.itworkscdn.net/aljadeedlive/aljadeedlive.smil/playlist.m3u8"),
    ("🌐 الجديد - Al Jadeed 2 [Internet]", "https://aljadeedlive.akamaihd.net/hls/live/202274/aljadeedlive/master.m3u8"),
    ("🌐 MTV Lebanon [Internet]", "https://mtvlebanon.akamaihd.net/hls/live/202771/mtvlebanon/master.m3u8"),
    ("🌐 LBCI Lebanon [Internet]", "https://lbci-live.akamaihd.net/hls/live/202274/lbci/master.m3u8"),
    ("🌐 OTV Lebanon [Internet]", "https://otv.akamaihd.net/hls/live/202274/otv/master.m3u8"),
    ("🌐 Al Manar [Internet]", "https://almanar.akamaihd.net/hls/live/202274/almanar/master.m3u8"),
    ("🌐 Al Mayadeen [Internet]", "https://wpc.c1a9.edgecastcdn.net/hls-live/20C1A9/almayadeen/live/almayadeen.m3u8"),
    ("🌐 Tele Liban [Internet]", "https://teleliban.akamaihd.net/hls/live/202274/teleliban/master.m3u8"),
]
for name, url in internet_only:
    inf = f'#EXTINF:-1 tvg-name="{name}" tvg-language="Arabic" tvg-country="LB" group-title="🌐 قنوات الإنترنت فقط",{name}'
    add(arabic, inf, url)
print(f"✅ زدنا قنوات الإنترنت - المجموع دوكا: {len(arabic)}")
print("2. Nilesat مشي عربية...")
nilesat = {}
nilesat_countries = ['eg','dz','ma','tn','ly','lb','jo','ps','sy','iq','tr','fr','it','es','de','gr','gb','nl','be','pl','ro','bg','hu','cz','at','ch','pt']
for code in nilesat_countries:
    lines = get_lines(f'https://iptv-org.github.io/iptv/countries/{code}.m3u')
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
            low = lines[i].lower()
            if 'language="arabic"' in low:
                continue
            name = lines[i].split(',')[-1]
            if any('\u0600' <= ch <= '\u06FF' for ch in name):
                continue
            url = lines[i+1].strip()
            if url in arabic:
                continue
            add(nilesat, lines[i], lines[i+1])
print(f"✅ 2. Nilesat مشي عربية: {len(nilesat)}")
print("3. Arabsat مشي عربية...")
arabsat = {}
arabsat_countries = ['sa','ae','qa','kw','bh','om','ye','eg','jo','iq','lb','sy','ir','pk','in','bd','id','my','af','et','ke','za','ng','sd']
for code in arabsat_countries:
    lines = get_lines(f'https://iptv-org.github.io/iptv/countries/{code}.m3u')
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
            low = lines[i].lower()
            if 'language="arabic"' in low:
                continue
            name = lines[i].split(',')[-1]
            if any('\u0600' <= ch <= '\u06FF' for ch in name):
                continue
            url = lines[i+1].strip()
            if url in arabic:
                continue
            add(arabsat, lines[i], lines[i+1])
print(f"✅ 3. Arabsat مشي عربية: {len(arabsat)}")
def save(filename, store):
    with open(filename,'w',encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for url, inf in store.items():
            f.write(inf + "\n" + url + "\n")
save('arabic.m3u', arabic)
save('nilesat.m3u', nilesat)
save('arabsat.m3u', arabsat)
save('channels.m3u', arabic)
print("🎉 كملنا:")
print(f"arabic.m3u = {len(arabic)}")
print(f"nilesat.m3u = {len(nilesat)}")
print(f"arabsat.m3u = {len(arabsat)}")
