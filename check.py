import requests, re
# 1. نقراو wanted.txt - الأسماء اللي عطيتهوملي
try:
    with open('wanted.txt',encoding='utf-8') as f:
        wanted = [l.strip() for l in f if l.strip() and not l.strip().startswith('    
except: wanted = []
print(f"مطلوب: {len(wanted)}")
                                                                       
SOURCES = [
    '#')]
except: wanted = []
print(f"مطلوب: {len(wanted)}")
# 2. نجيبو كل القنوات من iptv-org - كل الأقمار
SOURCES = [
    'https://iptv-org.github.io/iptv/index.m3u',                      
    '# كل الأقمار
    'https://iptv-org.github.io/iptv/regions/mena.m3u',                           
    '# MENA = Nilesat + Arabsat
    'https://iptv-org.github.io/iptv/regions/arab.m3u',                      
]
seen_url = set()
all_channels = []
available = {}
for url in SOURCES:
    try:
        r = requests.get(url, timeout=120, headers={'# كل العربية
]
seen_url = set()
all_channels = []
available = {}
for url in SOURCES:
    try:
        r = requests.get(url, timeout=120, headers={'User-Agent':'Mozilla/5.0'})
        parts = re.split(r'(?=#EXTINF)', r.text)
        for p in parts:
            if '                           
            lines = p.strip().splitlines()
            if len(lines) < 2: continue
            info = lines[0].strip(); stream = lines[1].strip()
            if not stream.startswith('#EXTINF' not in p: continue
            lines = p.strip().splitlines()
            if len(lines) < 2: continue
            info = lines[0].strip(); stream = lines[1].strip()
            if not stream.startswith('http'): continue
            if stream in seen_url: continue
            seen_url.add(stream)
            m = re.search(r',(.+)$', info)
            name = m.group(1).strip() if m else ""
            if len(name) < 2: continue
            all_channels.append((info, stream, name))
            key = re.sub(r'[^a-z0-9]', '', name.lower())
            if key not in available:
                available[key] = (info, stream, name)
    except Exception as e:
        print(f"فشل {url}: {e}")
print(f"الكل: {len(all_channels)}")
                                            
found = []; not_found = []
for w in wanted:
    wk = re.sub(r'# 3. نقارنو wanted مع المتوفر
found = []; not_found = []
for w in wanted:
    wk = re.sub(r'[^a-z0-9]', '', w.lower())
    match = None
    if wk in available:
        match = available[wk]
    else:
        for ak, (info, stream, aname) in available.items():
            if wk in ak or ak in wk:
                if len(wk) >= 4:
                    match = (info, stream, aname); break
    if match:
        info, stream, name = match
        found.append((info, stream, w))
        print(f"✅ {w}")
    else:
        not_found.append(w)
        print(f"❌ X - {w}")
print(f"لقينا: {len(found)} / ما لقيناش: {len(not_found)}")
                            
with open('# 4. نكتب الملفين
with open('nilesat-arabsat.m3u','w',encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    for info, stream, _ in found:
        f.write(f"{info}\n{stream}\n")
    for w in not_found:
        f.write(f"                                     
        f.write(f'                                              
        f.write(f"# ❌ X - {w} - غير موجود\n")
        f.write(f'#EXTINF:-1 group-title="❌ X",❌ X - {w}\n')
        f.write(f"https://example.com/not-found/{re.sub(r'[^a-z0-9]', '', w.lower())}.m3u8\n")
for fname in ['ta.m3u','arabic-working.m3u']:
    with open(fname,'w',encoding='utf-8') as out:
        with open('nilesat-arabsat.m3u',encoding='utf-8') as src:
            out.write(src.read())
print(f"كمل - {len(found)} ✅ + {len(not_found)} ❌ X")
