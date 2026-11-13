import requests

print("🚀 الروبوت بدأ - قنوات + أفلام + كرتون")

all_streams = {}

def add(inf, url):
    url = url.strip()
    if not url.startswith('http') or url in all_streams:
        return
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

# ===== 1. القنوات العربية =====
for code in ['dz','ma','tn','eg','sa','ae','qa','kw','jo','lb','iq','ye','ps','sy','ly','sd','mr','bh','om']:
    try:
        r = requests.get(f'https://iptv-org.github.io/iptv/countries/{code}.m3u', timeout=25, headers=headers)
        if r.status_code == 200:
            parse(r.text)
    except: pass
try:
    r = requests.get('https://iptv-org.github.io/iptv/languages/ara.m3u', timeout=25, headers=headers)
    if r.status_code == 200:
        parse(r.text)
    print(f"✅ القنوات: {len(all_streams)}")
except: pass

# ===== 2. أفلام ومسلسلات عربية =====
for cat, new_group in [('movies','🎬 أفلام'), ('series','📺 مسلسلات')]:
    try:
        r = requests.get(f'https://iptv-org.github.io/iptv/categories/{cat}.m3u', timeout=25, headers=headers)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for i in range(len(lines)):
                if lines[i].startswith('#EXTINF'):
                    if i+1 < len(lines) and lines[i+1].strip().startswith('http'):
                        name = lines[i].split(',')[-1]
                        if any('\u0600' <= ch <= '\u06FF' for ch in name) or 'arab' in name.lower():
                            # نبدل المجموعة
                            import re
                            inf = re.sub(r'group-title="[^"]*"', f'group-title="{new_group}"', lines[i])
                            if 'group-title=' not in inf:
                                inf = inf.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{new_group}"')
                            add(inf, lines[i+1].strip())
            print(f"✅ {new_group}: المجموع {len(all_streams)}")
    except: pass

# ===== 3. أفلام كرتون - منفصلين في مجموعة وحدها =====
print("جاري جمع الكرتون...")
cartoon_count = 0
# أ. من تصنيف animation و kids
for cat in ['animation','kids']:
    try:
        r = requests.get(f'https://iptv-org.github.io/iptv/categories/{cat}.m3u', timeout=25, headers=headers)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for i in range(len(lines)):
                if lines[i].startswith('#EXTINF'):
                    if i+1 < len(lines) and lines[i+1].strip().startswith('http'):
                        name = lines[i].split(',')[-1]
                        # غير العربي أو اللي اسمه كرتون
                        is_arabic = any('\u0600' <= ch <= '\u06FF' for ch in name)
                        is_cartoon_word = any(k in name.lower() for k in ['cartoon','anime','كرتون','انمي','انيمي','animation','disney','pixar','سبونج','توم وجيري'])
                        if is_arabic or is_cartoon_word:
                            import re
                            inf = re.sub(r'group-title="[^"]*"', 'group-title="🎨 أفلام كرتون"', lines[i])
                            if 'group-title=' not in inf:
                                inf = inf.replace('#EXTINF:-1', '#EXTINF:-1 group-title="🎨 أفلام كرتون"')
                            before = len(all_streams)
                            add(inf, lines[i+1].strip())
                            if len(all_streams) > before:
                                cartoon_count += 1
            print(f"✅ {cat} كرتون: +{cartoon_count}")
    except: pass

# ب. من الأفلام - اللي اسمه فيه كرتون نحولوه لمجموعة الكرتون
# نعاودو نفحصو قائمة الأفلام
try:
    r = requests.get('https://iptv-org.github.io/iptv/categories/movies.m3u', timeout=25, headers=headers)
    lines = r.text.splitlines()
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF'):
            if i+1 < len(lines) and lines[i+1].strip().startswith('http'):
                name = lines[i].split(',')[-1].lower()
                if any(k in name for k in ['cartoon','anime','كرتون','انمي','disney','pixar','animation','مدبلج','tom and jerry']):
                    import re
                    inf = re.sub(r'group-title="[^"]*"', 'group-title="🎨 أفلام كرتون"', lines[i])
                    if 'group-title=' not in inf:
                        inf = inf.replace('#EXTINF:-1', '#EXTINF:-1 group-title="🎨 أفلام كرتون"')
                    before = len(all_streams)
                    add(inf, lines[i+1].strip())
                    if len(all_streams) > before:
                        cartoon_count += 1
    print(f"✅ كرتون من الأفلام: المجموع {cartoon_count}")
except: pass

print(f"📊 المجموع الكامل: {len(all_streams)} | منها كرتون: {cartoon_count}")

# ===== حفظ كلش في ملف واحد =====
with open('arabic.m3u','w',encoding='utf-8') as f:
    f.write("#EXTM3U\n")
    for url, inf in all_streams.items():
        f.write(inf + "\n" + url + "\n")

print(f"✅ تم: arabic.m3u - {len(all_streams)}")
