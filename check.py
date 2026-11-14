import requests, re
from concurrent.futures import ThreadPoolExecutor

print("🚀 نبداو من الصفر - غير القنوات العربية الشغالة")

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
    if any(k in low for k in [' fm', 'fm ', '.mp3', 'radio ', 'إذاعة', 'اذاعة', 'راديو', 'quran radio', 'radio quran']):
        if ' tv' not in low and 'tv ' not in low and 'channel' not in low:
            return True
    return False

# ================= 1. نجمعو القنوات العربية برك =================
print("1. نجمعو القنوات العربية...")
arabic = {}

def add(inf, url):
    url = url.strip()
    if not url.startswith('http') or url in arabic:
        return
    if 'localhost' in url or 'example.com' in url:
        return
    if is_radio(inf, url):
        return
    inf = re.sub(r'group-title="[^"]*"', 'group-title="🇩🇿 القنوات العربية"', inf)
    if 'group-title=' not in inf:
        inf = inf.replace('#EXTINF:-1', '#EXTINF:-1 group-title="🇩🇿 القنوات العربية"')
    arabic[url] = inf.strip()

for code in ['dz','ma','tn','eg','sa','ae','qa','kw','jo','lb','iq','ye','ps','sy','ly','sd','mr','bh','om']:
    lines = get_lines(f'https://iptv-org.github.io/iptv/countries/{code}.m3u')
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
            add(lines[i], lines[i+1])

lines = get_lines('https://iptv-org.github.io/iptv/languages/ara.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        add(lines[i], lines[i+1])

print(f"📥 لقينا: {len(arabic)} قناة عربية قبل الفحص")

# ================= 2. قنوات الإنترنت فقط =================
print("🌐 نزيدو قنوات الإنترنت...")
internet_only = [
    ("🌐 الجديد - Al Jadeed [Internet]", "https://livestreaming.itworkscdn.net/aljadeedlive/aljadeedlive.smil/playlist.m3u8"),
    ("🌐 MTV Lebanon [Internet]", "https://mtvlebanon.akamaihd.net/hls/live/202771/mtvlebanon/master.m3u8"),
    ("🌐 LBCI Lebanon [Internet]", "https://lbci-live.akamaihd.net/hls/live/202274/lbci/master.m3u8"),
    ("🌐 OTV Lebanon [Internet]", "https://otv.akamaihd.net/hls/live/202274/otv/master.m3u8"),
    ("🌐 Al Manar [Internet]", "https://almanar.akamaihd.net/hls/live/202274/almanar/master.m3u8"),
    ("🌐 Al Mayadeen [Internet]", "https://wpc.c1a9.edgecastcdn.net/hls-live/20C1A9/almayadeen/live/almayadeen.m3u8"),
    ("🌐 Tele Liban [Internet]", "https://teleliban.akamaihd.net/hls/live/202274/teleliban/master.m3u8"),
]
for name, url in internet_only:
    inf = f'#EXTINF:-1 tvg-name="{name}" tvg-language="Arabic" tvg-country="LB" group-title="🇩🇿 القنوات العربية",{name}'
    if url not in arabic:
        arabic[url] = inf

print(f"📥 المجموع قبل الفحص: {len(arabic)}")

# ================= 3. نفحصو كل قناة - الشغالة برك =================
print("🔍 نفحصو كل قناة... هذا يأخذ 3-5 دقائق")

def is_working(url):
    try:
        r = requests.head(url, timeout=6, headers=headers, allow_redirects=True)
        if r.status_code == 200:
            return True
        if r.status_code in [403, 405, 301, 302]:
            pass
        else:
            r2 = requests.get(url, timeout=8, headers=headers, stream=True)
            if r2.status_code == 200:
                chunk = next(r2.iter_content(1024), b'')
                r2.close()
                if len(chunk) > 0:
                    return True
            return False
        r2 = requests.get(url, timeout=8, headers=headers, stream=True)
        if r2.status_code == 200:
            chunk = next(r2.iter_content(1024), b'')
            r2.close()
            if len(chunk) > 0:
                return True
        return False
    except:
        return False

urls = list(arabic.keys())
working = {}

with ThreadPoolExecutor(max_workers=50) as ex:
    results = list(ex.map(is_working, urls))

for url, ok in zip(urls, results):
    if ok:
        working[url] = arabic[url]

print(f"✅ الشغالة فقط: {len(working)} من {len(arabic)}")
print(f"❌ حذفنا الميتة: {len(arabic) - len(working)}")

# ================= 4. الحفظ - رابط واحد + كود =================
def save(filename, store):
    with open(filename,'w',encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for url, inf in store.items():
            f.write(inf + "\n" + url + "\n")

save('arabic.m3u', working)
save('channels.m3u', working)
save('all.m3u', working)
save('1111111111111122.m3u', working)
save('nilesat.m3u', {})
save('arabsat.m3u', {})

print("🎉 كملنا - غير القنوات العربية الشغالة")
print(f"arabic.m3u = {len(working)}")
print(f"all.m3u = {len(working)}")
print(f"1111111111111122.m3u = {len(working)} - الكود")
