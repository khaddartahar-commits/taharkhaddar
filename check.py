import requests, re

# 1. نقرا servers-all.txt
with open('servers-all.txt', encoding='utf-8') as f:
    urls = [l.strip() for l in f if l.strip().startswith('http')]

arabic = []
for url in urls:
    try:
        print(f"نجيب من: {url}")
        txt = requests.get(url, timeout=30).text
        # نقسمو القنوات
        blocks = re.split(r'(?=#EXTINF)', txt)
        for b in blocks:
            low = b.lower()
            # فلتر عربي: لغة عربية ولا دولة عربية ولا اسم عربي
            if 'ara' in low or 'arab' in low or 'dz' in low or 'ma,' in low or 'tn' in low or 'eg' in low or 'sa' in low or 'alger' in low or 'maroc' in low or 'tunis' in low or 'egypt' in low or 'saudi' in low or 'mbc' in low or 'al jazeera' in low:
                if '#EXTINF' in b:
                    arabic.append(b.strip())
    except Exception as e:
        print(f"فشل: {url} - {e}")

# 2. نحفظ النتيجة
with open('arabic-maghreb.m3u','w',encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    f.write('\n'.join(arabic))

print(f"لقينا {len(arabic)} قناة عربية")
