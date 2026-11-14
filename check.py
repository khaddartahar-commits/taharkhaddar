import requests, re

print("🚀 بدأ - ملفات منفصلة + رابط واحد")

headers = {'User-Agent': 'Mozilla/5.0'}

def get_lines(url):
    try:
        r = requests.get(url, timeout=25, headers=headers)
        if r.status_code == 200:
            return r.text.splitlines()
    except: pass
    return []

def set_group(inf, g):
    inf = re.sub(r'group-title="[^"]*"', f'group-title="{g}"', inf)
    if 'group-title=' not in inf:
        inf = inf.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{g}"')
    return inf

channels, movies, series, cartoon = {}, {}, {}, {}

def add(store, inf, url):
    url = url.strip()
    if not url.startswith('http') or url in store:
        return
    if 'localhost' in url or 'example.com' in url:
        return
    store[url] = inf.strip()

# --- 1. القنوات في ملف وحدو ---
for code in ['dz','ma','tn','eg','sa','ae','qa','kw','jo','lb','iq','ye','ps','sy','ly','sd','mr','bh','om']:
    lines = get_lines(f'https://iptv-org.github.io/iptv/countries/{code}.m3u')
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
            add(channels, lines[i], lines[i+1])
lines = get_lines('https://iptv-org.github.io/iptv/languages/ara.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        add(channels, lines[i], lines[i+1])

# --- 2. الأفلام في ملف وحدو ---
lines = get_lines('https://iptv-org.github.io/iptv/categories/movies.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        name = lines[i].split(',')[-1]
        low = name.lower()
        is_arabic = any('\u0600' <= ch <= '\u06FF' for ch in name)
        is_cartoon = any(k in low for k in ['cartoon','anime','كرتون','انمي','disney','pixar','animation','مدبلج'])
        if is_arabic or 'arab' in low:
            if is_cartoon:
                add(cartoon, set_group(lines[i], '🎨 أفلام كرتون'), lines[i+1])
            else:
                add(movies, set_group(lines[i], '🎬 أفلام'), lines[i+1])

# --- 3. المسلسلات في ملف وحدو ---
lines = get_lines('https://iptv-org.github.io/iptv/categories/series.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        name = lines[i].split(',')[-1]
        if any('\u0600' <= ch <= '\u06FF' for ch in name) or 'arab' in name.lower():
            add(series, set_group(lines[i], '📺 مسلسلات'), lines[i+1])

# --- 4. الكرتون في ملف وحدو ---
for cat in ['animation','kids']:
    lines = get_lines(f'https://iptv-org.github.io/iptv/categories/{cat}.m3u')
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
            name = lines[i].split(',')[-1]
            if any('\u0600' <= ch <= '\u06FF' for ch in name) or any(k in name.lower() for k in ['cartoon','anime','كرتون','disney']):
                add(cartoon, set_group(lines[i], '🎨 أفلام كرتون'), lines[i+1])

print(f"قنوات: {len(channels)} | أفلام: {len(movies)} | مسلسلات: {len(series)} | كرتون: {len(cartoon)}")

def save(name, store):
    with open(name,'w',encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for url, inf in store.items():
            f.write(inf + "\n" + url + "\n")
    print(f"✅ {name}: {len(store)}")

# نحفظو الملفات منفصلة
save('channels.m3u', channels)
save('movies.m3u', movies)
save('series.m3u', series)
save('cartoon.m3u', cartoon)

# ونزيدو نجمعوهم كامل في رابط واحد
all_combined = {}
all_combined.update(channels)
all_combined.update(movies)
all_combined.update(series)
all_combined.update(cartoon)
save('arabic.m3u', all_combined)

print(f"✅ الكل: arabic.m3u فيه {len(all_combined)}")
