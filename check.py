import requests, json, re, concurrent.futures

ARAB_COUNTRIES = ['DZ','MA','TN','EG','SA','AE','QA','KW','JO','LB','IQ','YE','PS','SY','LY','SD','MR','BH','OM','DZ']
ARAB_LANG = ['ara', 'ar']

print("🚀 بدأ الروبوت الأقوى - البحث عن كل القنوات العربية...")

all_streams = {}  # url -> extinf

def add_channel(name, group, url, country=''):
    if not url or not url.startswith('http'):
        return
    if url in all_streams:
        return
    # تنظيف الاسم
    name = name.strip()[:60]
    if not name:
        return
    group = group or 'عام'
    all_streams[url] = f'#EXTINF:-1 group-title="{group}" tvg-country="{country}",{name}'

# === مصدر 1: قاعدة iptv-org الكبيرة - 30 ألف قناة ===
try:
    print("📥 مصدر 1: تحميل قاعدة iptv-org...")
    r = requests.get('https://iptv-org.github.io/database/streams.json', timeout=30)
    data = r.json()
    print(f"   القاعدة فيها {len(data)} رابط")
    count = 0
    for s in data:
        url = s.get('url', '')
        ch = s.get('channel', '')
        # نجيبو غير العربية: اللغة عربية أو الدولة عربية
        # streams.json ما فيهش اللغة، نعتمدو على اسم القناة والقناة
        # الحل: نجيبو كلش ونفلترو بعد بالـ channels.json
        if url:
            # نحتفظو بيه مؤقتا، الفلترة في مصدر 2
            pass
    # نحمل channels.json باش نعرفو القنوات العربية
    rc = requests.get('https://iptv-org.github.io/database/channels.json', timeout=30)
    channels_data = {c['id']: c for c in rc.json()}
    arab_ids = set()
    for cid, c in channels_data.items():
        langs = c.get('languages') or []
        countries = c.get('countries') or []
        if any(l in ARAB_LANG for l in langs) or any(ct in ARAB_COUNTRIES for ct in countries):
            arab_ids.add(cid)
    print(f"   لقينا {len(arab_ids)} قناة عربية في القاعدة")
    for s in data:
        if s.get('channel') in arab_ids:
            url = s.get('url', '')
            # نجيبو اسم القناة من القاعدة
            ch_info = channels_data.get(s.get('channel'), {})
            name = ch_info.get('name', s.get('channel', 'قناة'))
            group = (ch_info.get('categories') or ['عام'])[0] if ch_info.get('categories') else 'عام'
            add_channel(name, group, url, '')
            count += 1
    print(f"✅ مصدر 1: {count} قناة عربية")
except Exception as e:
    print(f"❌ مصدر 1 فشل: {e}")

# === مصدر 2: قوائم الدول العربية ===
for code in ['dz','ma','tn','eg','sa','ae','qa','kw','jo','lb','iq','ye','ps','sy','ly','sd','mr','bh','om']:
    try:
        url = f"https://iptv-org.github.io/iptv/countries/{code}.m3u"
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code != 200:
            continue
        lines = r.text.splitlines()
        c = 0
        for i in range(len(lines)):
            if lines[i].startswith('#EXTINF'):
                if i+1 < len(lines) and lines[i+1].startswith('http'):
                    inf = lines[i]
                    stream_url = lines[i+1].strip()
                    name = inf.split(',')[-1].strip()
                    m = re.search(r'group-title="([^"]*)"', inf)
                    group = m.group(1) if m else 'عام'
                    add_channel(name, group, stream_url, code.upper())
                    c += 1
        print(f"✅ {code}: {c} قناة")
    except:
        pass

# === مصدر 3: قائمة اللغة العربية كاملة ===
try:
    r = requests.get('https://iptv-org.github.io/iptv/languages/ara.m3u', timeout=20)
    lines = r.text.splitlines()
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF'):
            if i+1 < len(lines) and lines[i+1].startswith('http'):
                inf = lines[i]
                name = inf.split(',')[-1].strip()
                m = re.search(r'group-title="([^"]*)"', inf)
                group = m.group(1) if m else 'عام'
                add_channel(name, group, lines[i+1].strip(), '')
    print(f"✅ مصدر اللغة العربية: تم")
except Exception as e:
    print(f"❌ مصدر اللغة: {e}")

# === مصدر 4: قوائم عالمية مجانية أخرى ===
EXTRA_LISTS = [
    'https://iptv-org.github.io/iptv/categories/news.m3u',
    'https://iptv-org.github.io/iptv/categories/sports.m3u',
    'https://iptv-org.github.io/iptv/categories/movies.m3u',
    'https://iptv-org.github.io/iptv/categories/kids.m3u',
    'https://iptv-org.github.io/iptv/categories/documentary.m3u',
    'https://iptv-org.github.io/iptv/categories/religious.m3u',
]
for list_url in EXTRA_LISTS:
    try:
        r = requests.get(list_url, timeout=15)
        lines = r.text.splitlines()
        for i in range(len(lines)):
            if lines[i].startswith('#EXTINF'):
                if i+1 < len(lines) and lines[i+1].startswith('http'):
                    # نجيبو غير اللي اسمها عربي أو فيها كلمات عربية
                    name = lines[i].split(',')[-1].strip()
                    # إذا الاسم فيه حروف عربية
                    if any('\u0600' <= ch <= '\u06FF' for ch in name):
                        m = re.search(r'group-title="([^"]*)"', lines[i])
                        group = m.group(1) if m else 'عام'
                        add_channel(name, group, lines[i+1].strip(), '')
        print(f"✅ {list_url.split('/')[-1]}: تم")
    except:
        pass

print(f"\n📊 المجموع قبل الفحص: {len(all_streams)} رابط")

# === الفحص السريع - ThreadPool باش يفحص 1000 في دقائق ===
def is_working(item):
    url, inf = item
    try:
        # نستعمل HEAD أولا، إذا فشل نستعمل GET صغير
        r = requests.head(url, timeout=6, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
        if r.status_code in [200, 301, 302, 403]:
            return (url, inf)
        r = requests.get(url, timeout=6, headers={'User-Agent': 'Mozilla/5.0'}, stream=True)
        if r.status_code == 200:
            return (url, inf)
    except:
        # بعض السيرفرات ترفض HEAD، نعتبروها شغالة إذا ما كانش Timeout طويل
        # نعاودو بـ GET
        try:
            r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'}, stream=True)
            if r.status_code == 200:
                return (url, inf)
        except:
            pass
    return None

print("🔍 جاري فحص كل الروابط... هاذي تاخذ 2-3 دقايق")
working = []
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
    results = list(ex.map(is_working, all_streams.items()))
    for res in results:
        if res:
            working.append(res)

print(f"✅ النتيجة النهائية: {len(working)} قناة شغالة")

# === تقسيم على 2 ملفات باش التطبيقات ما تتكسرش ===
# ملف 1: arabic.m3u - الكل
with open('arabic.m3u', 'w', encoding='utf-8') as out:
    out.write("#EXTM3U\n")
    for url, inf in working:
        out.write(inf + "\n" + url + "\n")

# ملف 2: arabic_1.m3u - أول 500
with open('arabic_1.m3u', 'w', encoding='utf-8') as out:
    out.write("#EXTM3U\n")
    for url, inf in working[:500]:
        out.write(inf + "\n" + url + "\n")

# ملف 3: arabic_2.m3u - الباقي
if len(working) > 500:
    with open('arabic_2.m3u', 'w', encoding='utf-8') as out:
        out.write("#EXTM3U\n")
        for url, inf in working[500:]:
            out.write(inf + "\n" + url + "\n")

print(f"تم توليد arabic.m3u ({len(working)}), arabic_1.m3u, arabic_2.m3u")
