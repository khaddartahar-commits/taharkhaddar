import requests, re

print("🚀 بدأ - قنوات عربية فقط")

headers = {'User-Agent': 'Mozilla/5.0'}

def get_lines(url):
    try:
        r = requests.get(url, timeout=25, headers=headers)
        if r.status_code == 200:
            return r.text.splitlines()
    except:
        pass
    return []

channels = {}

def add(inf, url):
    url = url.strip()
    if not url.startswith('http') or url in channels:
        return
    if 'localhost' in url or 'example.com' in url:
        return
    channels[url] = inf.strip()

# --- كل الدول العربية ---
countries = ['dz','ma','tn','eg','sa','ae','qa','kw','jo','lb','iq','ye','ps','sy','ly','sd','mr','bh','om']

for code in countries:
    print(f"نجيبو {code}...")
    lines = get_lines(f'https://iptv-org.github.io/iptv/countries/{code}.m3u')
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
            add(lines[i], lines[i+1])

# --- كل القنوات اللي لغتها عربية ---
print("نجيبو اللغة العربية...")
lines = get_lines('https://iptv-org.github.io/iptv/languages/ara.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        add(lines[i], lines[i+1])

# --- كل منطقة الشرق الأوسط وشمال إفريقيا ---
print("نجيبو MENA...")
lines = get_lines('https://iptv-org.github.io/iptv/regions/mena.m3u')
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF') and i+1 < len(lines) and lines[i+1].strip().startswith('http'):
        add(lines[i], lines[i+1])

print(f"✅ المجموع: {len(channels)} قناة عربية")

# --- الحفظ ---
# رابط واحد برك، فيه غير القنوات
with open('arabic.m3u','w',encoding='utf-8') as f:
    f.write("#EXTM3U\n")
    for url, inf in channels.items():
        f.write(inf + "\n" + url + "\n")

with open('channels.m3u','w',encoding='utf-8') as f:
    f.write("#EXTM3U\n")
    for url, inf in channels.items():
        f.write(inf + "\n" + url + "\n")

print("🎉 كملنا - arabic.m3u = channels.m3u = قنوات فقط")
