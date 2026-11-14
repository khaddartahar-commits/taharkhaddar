# fix.py - يصلح كل الأكواد بلا ما يمس check.py
import os, re, glob

print("=== بدا الإصلاح ===")

# 1. نجيبو كل ملفات m3u
files = glob.glob("*.m3u")
print(f"لقينا {len(files)} ملف m3u: {files}")

def clean_m3u(fname):
    try:
        with open(fname, encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except:
        print(f"❌ ما قدرناش نفتحو {fname}")
        return []
    # نقسمو القنوات
    parts = re.split(r'(?=#EXTINF)', text)
    seen = set()
    clean = []
    for p in parts:
        if '#EXTINF' not in p:
            continue
        lines = p.strip().splitlines()
        if len(lines) < 2:
            continue
        info = lines[0].strip()
        url = lines[1].strip()
        # إصلاح 1: نحذفو الروابط المكسرة
        if not url.startswith('http'):
            continue
        if len(url) < 10:
            continue
        # إصلاح 2: نحذفو المكرر بنفس الرابط
        if url in seen:
            continue
        seen.add(url)
        # إصلاح 3: اذا الاسم فارغ نديرو اسم من الرابط
        if ',' not in info or info.split(',')[-1].strip() == '':
            info = info + ' قناة'
        # إصلاح 4: نصلحو اللوغو اذا مكسور
        if 'tvg-logo=""' in info:
            info = info.replace('tvg-logo=""', 'tvg-logo="https://via.placeholder.com/70?text=TV"')
        clean.append((info, url))
    # نعاودو نكتبو الملف نظيف
    with open(fname, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for info, url in clean:
            f.write(f"{info}\n{url}\n")
    print(f"✅ {fname} -> {len(clean)} قناة نظيفة (قبل كان فيه {len(parts)} سطر)")
    return clean

all_clean = {}
for fname in files:
    if fname == 'ta.m3u':
        continue
    all_clean[fname] = clean_m3u(fname)

# 2. نعاودو نبنو ta.m3u من كل الملفات النظيفة
print("=== نبنو ta.m3u جديد ===")
seen_all = set()
ta_list = []
for fname, lst in all_clean.items():
    for info, url in lst:
        if url not in seen_all:
            seen_all.add(url)
            ta_list.append((info, url))

with open('ta.m3u', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    for info, url in ta_list:
        f.write(f"{info}\n{url}\n")
print(f"✅ ta.m3u الجديد = {len(ta_list)} قناة كل الدول")

# 3. نصلحو أسماء الملفات المزدوجة - France.m3u و france.m3u نفس الشي
# ننسخو الكبير للصغير باش ما يبقاش واحد فارغ
pairs = [
    ('France.m3u', 'french-working.m3u'),
    ('Italie.m3u', 'italie.m3u'),
    ('Espagne.m3u', 'espagne.m3u'),
    ('Allemagne.m3u', 'allemagne.m3u'),
    ('Angleterre.m3u', 'angleterre.m3u'),
    ('Portugal.m3u', 'portugal.m3u'),
    ('Hollande.m3u', 'hollande.m3u'),
]
for big, small in pairs:
    try:
        if os.path.exists(big):
            with open(big, encoding='utf-8') as f: data = f.read()
            with open(small, 'w', encoding='utf-8') as f: f.write(data)
            print(f"✅ نسخنا {big} -> {small}")
    except Exception as e:
        print(f"❌ {big}: {e}")

# 4. نتأكدو بلي الملفات المهمة كاينين و ماشي فارغين
for must in ['ta.m3u','arabic-working.m3u','France.m3u','Italie.m3u','Espagne.m3u','Allemagne.m3u','Angleterre.m3u','Portugal.m3u','Hollande.m3u']:
    if not os.path.exists(must):
        with open(must, 'w', encoding='utf-8') as f: f.write('#EXTM3U\n')
        print(f"⚠️ خلقنا {must} كان ناقص")
    else:
        size = os.path.getsize(must)
        print(f"📄 {must} = {size} byte")

print("=== كمل الإصلاح كلش ===")
