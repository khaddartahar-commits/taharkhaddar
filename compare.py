print("📊 مقارنة القنوات الشغالة")

our = []
try:
    with open('arabic.m3u', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#EXTINF'):
                our.append(line.split(',')[-1].strip().lower())
except:
    our = []

checks = ["MBC 1","MBC 2","MBC 3","Al Jazeera","Rotana Cinema","CBC","DMC","ON TV","Nile Cinema","Dubai TV","Ennahar TV","Echorouk TV","2M","Al Aoula","Spacetoon","BBC Arabic","Al Jadeed","MTV Lebanon","LBCI","Al Manar"]

def exists(n):
    n = n.lower()
    for o in our:
        if n in o or o in n:
            return True
    return False

with open('compare_nilesat_arabsat.md','w',encoding='utf-8') as f:
    f.write("# ✅ القنوات العربية الشغالة فقط\n\n")
    f.write(f"عدد القنوات الشغالة: **{len(our)}**\n\n")
    f.write(f"الكود: **1111111111111122**\n\n")
    f.write("| القناة | الحالة |\n")
    f.write("| --- | --- |\n")
    for name in checks:
        f.write(f"| {name} | {'✅ شغالة' if exists(name) else '❌ ميتة / ناقصة'} |\n")

print(f"✅ كملت: {len(our)} قناة شغالة")
