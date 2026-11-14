import re

print("📊 بدأ المقارنة Nilesat / Arabsat")

our_channels = []
try:
    with open('arabic.m3u', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#EXTINF'):
                name = line.split(',')[-1].strip().lower()
                our_channels.append(name)
except:
    our_channels = []

def exists(name_list, our):
    for n in name_list:
        n = n.lower().strip()
        for o in our:
            if n in o or o in n:
                return True
            clean_n = re.sub(r'[^a-z0-9\u0600-\u06FF]', '', n)
            clean_o = re.sub(r'[^a-z0-9\u0600-\u06FF]', '', o)
            if clean_n and clean_n in clean_o:
                return True
    return False

nilesat = [
    "MBC 1", "MBC 2", "MBC 3", "MBC 4", "MBC Action", "MBC Drama", "MBC Max", "MBC Bollywood",
    "Al Jazeera", "Al Jazeera Documentary", "Al Arabiya", "Al Hadath",
    "Rotana Cinema", "Rotana Classic", "Rotana Drama", "Rotana Music", "Rotana Khalijia",
    "CBC", "CBC Drama", "DMC", "DMC Drama", "ON TV", "ON Drama", "Al Nahar", "Al Nahar Drama",
    "Nile TV", "Nile Cinema", "Nile Drama", "Nile Comedy", "Nile Sport",
    "Dubai TV", "Dubai One", "Abu Dhabi TV", "Abu Dhabi Sport 1", "Sharjah TV",
    "Algeria TV", "Canal Algerie", "Algeria 3", "Ennahar TV", "Echorouk TV", "Samira TV",
    "Morocco 2M", "Al Aoula", "Tunisia Nessma", "Tunisia Hannibal",
    "Al Qahera", "Al Kahera Wal Nas", "Sada El Balad", "Al Hayat",
    "Spacetoon", "Majid Kids", "Baraem", "Jeem TV",
    "Zee Alwan", "Zee Aflam", "ART Cinema", "ART Hekayat", "OSN Movies",
    "BBC Arabic", "France 24 Arabic", "DW Arabic", "Sky News Arabia",
    "beIN Sports 1", "beIN Sports 2", "beIN Movies",
    "Iqraa", "Al Majd", "Noor Dubai", "Quran Kareem"
]

arabsat = [
    "MBC 1", "MBC 2", "MBC 3", "MBC Action", "MBC Drama", "MBC Pro Sports",
    "Saudi TV 1", "Saudi TV 2", "Saudi Quran", "Saudi Sunnah", "Al Ekhbariya",
    "Al Jazeera", "Al Arabiya", "Al Hadath",
    "Rotana Cinema", "Rotana Khalijia", "Rotana Music",
    "Dubai TV", "Abu Dhabi TV", "Sharjah TV", "Kuwait TV", "Qatar TV", "Bahrain TV", "Oman TV",
    "Jordan TV", "Lebanon LBC", "Lebanon MTV", "Iraq Al Sharqiya", "Syria TV",
    "beIN Sports 1", "beIN Sports 2", "beIN Sports 3", "beIN Movies",
    "Al Majd", "Iqraa", "Noor Dubai", "Quran Kareem", "Sunnah",
    "BBC Arabic", "France 24 Arabic", "DW Arabic", "Sky News Arabia",
    "Spacetoon", "Majid Kids",
    "Al Qahera", "CBC", "DMC", "ON TV",
    "Nile TV", "Nile Cinema", "Nile Sport",
    "2M Morocco", "Al Aoula", "Tunisia Nessma"
]

nilesat = sorted(set(nilesat))
arabsat = sorted(set(arabsat))
all_names = sorted(set(nilesat + arabsat))

with open('compare_nilesat_arabsat.md','w',encoding='utf-8') as f:
    f.write("# 📡 مقارنة القنوات - Nilesat / Arabsat / قائمتنا\n\n")
    f.write(f"عدد قنواتنا في arabic.m3u: **{len(our_channels)}**\n\n")
    f.write("| القناة | Nilesat | Arabsat | عندنا ؟ |\n")
    f.write("| --- | --- | --- | --- |\n")
    found = 0
    missing = []
    for name in all_names:
        in_nile = "✅" if name in nilesat else "—"
        in_arab = "✅" if name in arabsat else "—"
        in_ours = exists([name], our_channels)
        in_ours_txt = "✅ موجودة" if in_ours else "❌ ناقصة"
        if in_ours:
            found += 1
        else:
            missing.append(name)
        f.write(f"| {name} | {in_nile} | {in_arab} | {in_ours_txt} |\n")
    f.write(f"\n## النتيجة\n")
    f.write(f"- ✅ موجودة عندنا: **{found} / {len(all_names)}**\n")
    f.write(f"- ❌ ناقصة عندنا: **{len(missing)}**\n\n")
    if missing:
        f.write("### القنوات الناقصة:\n")
        for m in missing:
            f.write(f"- {m}\n")

print(f"✅ كملت المقارنة: موجودة {found} / {len(all_names)}")
