import json, glob, requests

all_channels = []
for f in sorted(glob.glob('channels_*.json')):
    with open(f, encoding='utf-8') as fp:
        all_channels.extend(json.load(fp))

print(f"المجموع: {len(all_channels)} قناة من {len(glob.glob('channels_*.json'))} ملفات")

working = []
for ch in all_channels:
    try:
        r = requests.get(ch['url'], timeout=7, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            print(f"✅ {ch['name']}")
            working.append(ch)
        else:
            print(f"❌ {ch['name']} - {r.status_code}")
    except:
        print(f"❌ {ch['name']} - timeout")

# إزالة التكرار
seen=set(); uniq=[]
for c in working:
    if c['url'] not in seen:
        seen.add(c['url']); uniq.append(c)

with open('arabic.m3u','w',encoding='utf-8') as out:
    out.write("#EXTM3U\n")
    for ch in uniq:
        out.write(f"#EXTINF:-1 group-title=\"{ch['group']}\" tvg-country=\"{ch['country']}\",{ch['name']}\n{ch['url']}\n")

print(f"النتيجة: {len(uniq)}/{len(all_channels)} قناة شغالة -> arabic.m3u")
