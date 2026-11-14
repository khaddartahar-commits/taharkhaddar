import re
print("📊 مقارنة Nilesat / Arabsat")
our = []
try:
    with open('arabic.m3u', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#EXTINF'):
                our.append(line.split(',')[-1].strip().lower())
except:
    our = []
def exists(n):
    n = n.lower()
    for o in our:
        if n in o or o in n:
            return True
    return False
nilesat_list = ["MBC 1","MBC 2","MBC 3","MBC Action","MBC Drama","Al Jazeera","Rotana Cinema","CBC","DMC","ON TV","Al Nahar","Nile Cinema","Dubai TV","Abu Dhabi TV","Ennahar TV","Echorouk TV","2M","Al Aoula","Nessma","Spacetoon","BBC Arabic","beIN Sports 1","Iqraa","Al Majd","Al Jadeed","MTV Lebanon","LBCI"]
arabsat_list = ["MBC 1","MBC 2","Saudi TV 1","Saudi Quran","Saudi Sunnah","Al Ekhbariya","Al Jazeera","Rotana Cinema","Dubai TV","Kuwait TV","Qatar TV","beIN Sports 1","BBC Arabic","Spacetoon","Nile Cinema","CBC","DMC"]
all_names = sorted(set(nilesat_list + arabsat_list))
with open('compare_nilesat_arabsat.md','w',encoding='utf-8') as f:
    f.write("# 📡 مقارنة القنوات - Nilesat / Arabsat / قائمتنا\n\n")
    f.write(f"عدد قنواتنا العربية: **{len(our)}**\n\n")
    f.write("| القناة | Nilesat | Arabsat | عندنا ؟ |\n")
    f.write("| --- | --- | --- | --- |\n")
    found = 0
    missing = []
    for name in all_names:
        in_nile = "✅" if name in nilesat_list else "—"
        in_arab = "✅" if name in arabsat_list else "—"
        in_ours = exists(name)
        if in_ours:
            found += 1
        else:
            missing.append(name)
        f.write(f"| {name} | {in_nile} | {in_arab} | {'✅ موجودة' if in_ours else '❌ ناقصة'} |\n")
    f.write(f"\n## النتيجة\n")
    f.write(f"- ✅ موجودة: **{found} / {len(all_names)}**\n")
    f.write(f"- ❌ ناقصة: **{len(missing)}**\n")
    if missing:
        f.write("\n### الناقصة:\n")
        for m in missing:
            f.write(f"- {m}\n")
print(f"✅ كملت المقارنة: {found} / {len(all_names)}")
