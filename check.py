import requests, re

print("🚀 بدأ - ملفات منفصلة + رابط واحد")

headers = {'User-Agent': 'Mozilla/5.0'}

def get_lines(url):
    try:
        r = requests.get(url, timeout=25, headers=headers)
        if r.status_code == 200:
            return r.text.splitlines()
    except:
        pass
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

def is_arabic_text(name):
    return any('\u0600' <= ch <= '\u06FF' for ch in name)

# ================= 1. القنوات =================
print("1. القنوات...")
for code in ['dz','ma','tn','eg','sa','ae','qa','kw','jo','lb','iq','ye','ps','sy','ly','sd','mr','bh','om']:
    lines = get_lines(f'https://iptv-org.github.io/iptv/countries/{code}.m3u')
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
            add(channels, lines[i], lines[i+1])

lines = get_lines('https://iptv-org.github.io/iptv/languages/ara.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        add(channels, lines[i], lines[i+1])

print(f"✅ قنوات: {len(channels)}")

# ================= 2. الأفلام =================
print("2. الأفلام...")
lines = get_lines('https://iptv-org.github.io/iptv/categories/movies.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        name = lines[i].split(',')[-1]
        low = name.lower()
        # غير العربي
        if not is_arabic_text(name) and 'arab' not in low:
            continue
        # إذا كان كرتون نبعثوه للكرتون ماشي للأفلام
        is_cartoon_word = any(k in low for k in ['cartoon','anime','كرتون','انمي','disney','pixar','animation','مدبلج','توم وجيري','سبونج'])
        if is_cartoon_word:
            continue
        add(movies, set_group(lines[i], '🎬 أفلام'), lines[i+1])

print(f"✅ أفلام: {len(movies)}")

# ================= 3. المسلسلات =================
print("3. المسلسلات...")
lines = get_lines('https://iptv-org.github.io/iptv/categories/series.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        name = lines[i].split(',')[-1]
        low = name.lower()
        if not is_arabic_text(name) and 'arab' not in low:
            continue
        add(series, set_group(lines[i], '📺 مسلسلات'), lines[i+1])

print(f"✅ مسلسلات: {len(series)}")

# ================= 4. أفلام كرتون - غير بالعربية =================
print("4. الكرتون - عربي برك...")

def is_arabic_cartoon(name):
    low = name.lower()
    has_arabic = is_arabic_text(name)
    has_dubbed = any(k in low for k in ['مدبلج','مدبلجة','بالعربية','بالعربي','arab','عربي','arabic','دبلجة'])
    has_arabic_channel = any(k in low for k in ['spacetoon','سبيستون','mbc3','mbc 3','cartoon network arabia','cn arabia','كرتون','أطفال'])
    # إذا كان إنجليزي صافي نرفضوه
    if not has_arabic and not has_dubbed and not has_arabic_channel:
        return False
    # لازم يكون كرتون
    is_cartoon = any(k in low for k in ['cartoon','anime','كرتون','انمي','disney','pixar','animation','spacetoon','سبيستون','mbc3','توم وجيري','سبونج','مدبلج'])
    return is_cartoon or has_arabic_channel

# أ. من الأفلام
lines = get_lines('https://iptv-org.github.io/iptv/categories/movies.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        name = lines[i].split(',')[-1]
        if is_arabic_cartoon(name):
            add(cartoon, set_group(lines[i], '🎨 أفلام كرتون - عربي'), lines[i+1])

# ب. من animation و kids - غير العربي برك
for cat in ['animation','kids']:
    lines = get_lines(f'https://iptv-org.github.io/iptv/categories/{cat}.m3u')
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
            name = lines[i].split(',')[-1]
            if is_arabic_cartoon(name):
                add(cartoon, set_group(lines[i], '🎨 أفلام كرتون - عربي'), lines[i+1])

# ج. من القنوات العربية - سبيستون و MBC3 و CN Arabia
for code in ['sa','eg','ae','dz']:
    lines = get_lines(f'https://iptv-org.github.io/iptv/countries/{code}.m3u')
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
            name = lines[i].split(',')[-1].lower()
            if any(k in name for k in ['spacetoon','سبيستون','mbc3','mbc 3','cartoon network arabia','cn arabia']):
                add(cartoon, set_group(lines[i], '🎨 أفلام كرتون - عربي'), lines[i+1])

print(f"✅ كرتون عربي برك: {len(cartoon)}")

# ================= 5. الحفظ =================
def save(name, store):
    with open(name,'w',encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for url, inf in store.items():
            f.write(inf + "\n" + url + "\n")
    print(f"✅ {name}: {len(store)}")

# الملفات منفصلة
save('channels.m3u', channels)
save('movies.m3u', movies)
save('series.m3u', series)
save('cartoon.m3u', cartoon)

# رابط واحد يجمعهم كامل
all_combined = {}
all_combined.update(channels)
all_combined.update(movies)
all_combined.update(series)
all_combined.update(cartoon)
save('arabic.m3u', all_combined)

print(f"🎉 كملنا - الكل في arabic.m3u: {len(all_combined)}")
