import requests, re, concurrent.futures

# 1. نقراو السيرفرات
urls = []
for fname in ['servers-all.txt', 'servers-backup.txt']:
    try:
        with open(fname, encoding='utf-8', errors='ignore') as f:
            for l in f:
                l=l.strip()
                if l.startswith('http'):
                    urls.append(l)
    except: pass

print(f"لقينا {len(urls)} سيرفر")

# 2. نجبدو القنوات
all_channels = {} # نمنعو التكرار بالاسم

def is_arabic(info, url):
    low = (info + " " + url).lower()
    arab_words = ['ara', 'arab', 'alger', 'dz', 'maroc', 'ma,', 'tunis', 'tn', 'egypt', 'eg', 'saudi', 'sa', 'mbc', 'jazeera', 'maghreb', 'mashreq', 'beinsport', 'bein', 'ssc', 'qatar', 'kuwait', 'iraq', 'jordan', 'lebanon', 'syria', 'yemen', 'oman', 'bahrain', 'libya', 'sudan', 'mauritania', 'palestine']
    return any(w in low for w in arab_words)

for surl in urls:
    try:
        print(f"نجيب من: {surl}")
        r = requests.get(surl, timeout=30, headers={'User-Agent':'Mozilla/5.0'})
        text = r.text
        # نقسمو على كل قناة
        parts = re.split(r'(?=#EXTINF)', text)
        for p in parts:
            if '#EXTINF' not in p: continue
            lines = p.strip().splitlines()
            if len(lines) < 2: continue
            info = lines[0]
            stream = lines[1].strip()
            if not stream.startswith('http'): continue
            if is_arabic(info, stream):
                # نجيبو الاسم
                m = re.search(r',(.+)$', info)
                name = m.group(1).strip() if m else stream
                if name not in all_channels:
                    all_channels[name] = (info, stream)
    except Exception as e:
        print(f"فشل {surl}: {e}")

print(f"لقينا {len(all_channels)} قناة عربية قبل الفحص")

# 3. نفحصو واش شغالة ولا لا
def is_working(item):
    name, (info, stream) = item
    try:
        r = requests.head(stream, timeout=8, allow_redirects=True, headers={'User-Agent':'Mozilla/5.0'})
        if r.status_code < 400:
            return item
        # بعض السيرفرات ما يقبلوش HEAD، نجربو GET خفيف
        r2 = requests.get(stream, timeout=8, stream=True, headers={'User-Agent':'Mozilla/5.0', 'Range':'bytes=0-1000'})
        if r2.status_code < 400:
            return item
    except:
        pass
    return None

working = []
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
    for res in ex.map(is_working, list(all_channels.items())):
        if res:
            working.append(res)
            print(f"✅ شغالة: {res[0]}")

print(f"بقاو {len(working)} قناة شغالة")

# 4. نقسمو مغرب / مشرق
maghreb_keys = ['alger','dz','maroc','ma,','tunis','tn','libya','mauritania','morocco']
maghreb = []
mashreq = []

for name, (info, stream) in working:
    low = (name + " " + info).lower()
    if any(k in low for k in maghreb_keys):
        maghreb.append((info, stream))
    else:
        mashreq.append((info, stream))

def write_m3u(fname, lst):
    with open(fname, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for info, stream in lst:
            f.write(f"{info}\n{stream}\n")

# الملف الواحد اللي حبيتو - غير الشغالة
write_m3u('arabic-working.m3u', working)
write_m3u('arabic-maghreb.m3u', maghreb)
write_m3u('arabic-mashreq.m3u', mashreq)

print(f"تم: working={len(working)} maghreb={len(maghreb)} mashreq={len(mashreq)}")
