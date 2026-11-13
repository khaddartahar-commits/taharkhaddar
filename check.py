import requests, re, time

print("🚀 الروبوت بدأ - البحث عن القنوات العربية")

all_streams = {}

def add(inf, url):
    url = url.strip()
    if not url.startswith('http'):
        return
    if url in all_streams:
        return
    # نمنع الروابط الميتة المعروفة
    if 'localhost' in url or 'example.com' in url:
        return
    all_streams[url] = inf.strip()

def parse(text):
    lines = text.splitlines()
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF'):
            if i+1 < len(lines) and lines[i+1].strip().startswith('http'):
                add(lines[i], lines[i+1].strip())

headers = {'User-Agent': 'Mozilla/5.0'}

# --- المصدر 1: كل الدول العربية ---
countries = ['dz','ma','tn','eg','sa','ae','qa','kw','jo','lb','iq','ye','ps','sy','ly','sd','mr','bh','om']
for code in countries:
    try:
        r = requests.get(f'https://iptv-org.github.io/iptv/countries/{code}.m3u', timeout=25, headers=headers)
        if r.status_code == 200:
            before = len(all_streams)
            parse(r.text)
            print(f"✅ {code}: +{len(all_streams)-before} -> المجموع {len(all_streams)}")
    except Exception as e:
        print(f"❌ {code}: {e}")

# --- المصدر 2: اللغة العربية كاملة ---
try:
    r = requests.get('https://iptv-org.github.io/iptv/languages/ara.m3u', timeout=25, headers=headers)
    if r.status_code == 200:
        before = len(all_streams)
        parse(r.text)
        print(f"✅ ara: +{len(all_streams)-before} -> المجموع {len(all_streams)}")
except Exception as e:
    print(f"❌ ara: {e}")

# --- المصدر 3: التصنيفات - نجيبو غير اللي اسمها عربي ---
for cat in ['news','sports','movies','kids','documentary','religious','general','entertainment','series']:
    try:
        r = requests.get(f'https://iptv-org.github.io/iptv/categories/{cat}.m3u', timeout=25, headers=headers)
        if r.status_code == 200:
            lines = r.text.splitlines()
            added = 0
            for i in range(len(lines)):
                if lines[i].startswith('#EXTINF'):
                    if i+1 < len(lines) and lines[i+1].strip().startswith('http'):
                        name = lines[i].split(',')[-1]
                        if any('\u0600' <= ch <= '\u06FF' for ch in name):
                            before = len(all_streams)
                            add(lines[i], lines[i+1])
                            if len(all_streams) > before:
                                added += 1
            print(f"✅ {cat}: +{added} -> المجموع {len(all_streams)}")
    except:
        pass

# --- المصدر 4: قنوات مضمونة 100% ---
extra = [
    ('#EXTINF:-1 group-title="أخبار",Al Jazeera', 'https://live-hls-web-aje.getaj.net/AJE/index.m3u8'),
    ('#EXTINF:-1 group-title="أخبار",France 24 عربي', 'https://cdn.klowdtv.net/803B48A/n1.klowdtv.net/live1/france24_oori/smil:france24_oori.smil/playlist.m3u8'),
    ('#EXTINF:-1 group-title="أخبار",DW عربي', 'https://dwamdstream104.akamaized.net/hls/live/2015535/dwamdstream104/index.m3u8'),
    ('#EXTINF:-1 group-title="أخبار",Sky News عربية', 'https://stream.skynewsarabia.com/hls/sna.m3u8'),
    ('#EXTINF:-1 group-title="أخبار",Al Jazeera Mubasher', 'https://live-hls-web-ajm.getaj.net/AJM/index.m3u8'),
    ('#EXTINF:-1 group-title="أخبار",Al Jazeera Documentary', 'https://live-hls-web-ajd.getaj.net/AJD/index.m3u8'),
]
for inf, url in extra:
    add(inf, url)

print(f"\n📊 المجموع النهائي: {len(all_streams)} قناة")

# --- الكتابة ---
with open('arabic.m3u', 'w', encoding='utf-8') as f:
    f.write("#EXTM3U\n")
    for url, inf in all_streams.items():
        f.write(inf + "\n" + url + "\n")

print(f"✅ تم حفظ arabic.m3u - {len(all_streams)} قناة")
