import requests, re

# نقراو السيرفرات - نستعملو غير السيرفرات الصغيرة الشغالة، ماشي الكبيرة اللي فيها 7000
urls=[]
for fname in ['servers-all.txt','servers-backup.txt']:
    try:
        with open(fname,encoding='utf-8',errors='ignore') as f:
            for l in f:
                l=l.strip()
                if l.startswith('http'): urls.append(l)
    except: pass
print(f"سيرفرات: {len(urls)}")

# هاذي هي اللغات و التصنيف تاعها
def get_lang(info, url):
    low = (info+" "+url).lower()
    if any(w in low for w in ['ara','arab','alger','dz','maroc','tunis','egypt','saudi','mbc','jazeera','bein','ssc','qatar','iraq','jordan','lebanon','syria','kuwait','yemen','oman','bahrain','libya','sudan','palestine','maghreb','mashreq','entv','echourouk','ennahar','samira','el heddaf']): return "AR"
    if any(w in low for w in ['fra','france','tf1','france 2','france 3','m6','bfm','lci','arte','canal+','cnews','tv5']): return "FR"
    if any(w in low for w in ['ita','italy','italia','rai','canale 5','italia 1','rete 4','la7','mediaset']): return "IT"
    if any(w in low for w in ['spa','spain','espa','antena 3','telecinco','cuatro','la sexta','movistar']): return "ES"
    if any(w in low for w in ['ger','germany','deutschland','ard','zdf','rtl','pro7','sat.1','vox']): return "DE"
    if any(w in low for w in ['uk','bbc','itv','channel 4','sky sports','sky uk','sky news','bt sport','tnt sports']): return "UK"
    if any(w in low for w in ['por','portugal','rtp','sic','tvi','sport tv','benfica']): return "PT"
    if any(w in low for w in ['nld','netherlands','holland','npo','rtl 4','ziggo','espn nl']): return "NL"
    return "OTHER"

def get_cat(info, url):
    low = (info+" "+url).lower()
    if any(w in low for w in ['sport','bein','ssc','espn','dazn','canal+ sport','lequipe','sky sport','eurosport']): return "Sports"
    if any(w in low for w in ['news','jazeera','france 24','bfm','lci','cnews','bbc news','sky news','cnn','al arabiya','sky news arabia']): return "News"
    if any(w in low for w in ['movie','cinema','film','cine','tcm','action','warner','hbo','netflix']): return "Movies"
    if any(w in low for w in ['kids','cartoon','disney','nick','gulli','tiji','canal j']): return "Kids"
    if any(w in low for w in ['music','mtv','mcm','nrj hits','trace','melody']): return "Music"
    if any(w in low for w in ['doc','discovery','national geo','planete','histoire','ushuaia']): return "Documentary"
    return "General"

groups = {}  # مثلا groups['AR - Sports'] = [...]
all_channels = []

for surl in urls:
    try:
        r = requests.get(surl, timeout=40, headers={'User-Agent':'Mozilla/5.0'})
        print(f"{surl[:60]} -> {len(r.text)}")
        parts = re.split(r'(?=#EXTINF)', r.text)
        for p in parts:
            if '#EXTINF' not in p: continue
            lines = p.strip().splitlines()
            if len(lines) < 2: continue
            info = lines[0]; stream = lines[1].strip()
            if not stream.startswith('http'): continue
            if '.m3u' in stream: continue  # نحذفو القوائم داخل القوائم
            m = re.search(r',(.+)$', info); name = m.group(1).strip() if m else stream
            if len(name) < 2: continue
            lang = get_lang(info, stream)
            cat = get_cat(info, stream)
            # هنا نبدلو group-title باش Televizo يصنف حسب اللغة
            # مثلا: group-title="AR - Sports"
            lang_name = {"AR":"Arabic","FR":"France","IT":"Italie","ES":"Espagne","DE":"Allemagne","UK":"Angleterre","PT":"Portugal","NL":"Hollande","OTHER":"Other"}[lang]
            new_group = f"{lang_name} - {cat}"
            # نعاودو نبنو سطر EXTINF جديد نظيف
            logo = ""
            lm = re.search(r'tvg-logo="([^"]+)"', info)
            if lm: logo = lm.group(1)
            new_info = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{new_group}",{name}'
            key = stream
            if key not in [c[1] for c in all_channels]:
                all_channels.append((new_info, stream, lang, cat))
                if new_group not in groups: groups[new_group] = []
                groups[new_group].append((new_info, stream))
    except Exception as e:
        print(f"فشل {surl}: {e}")

print(f"الكل: {len(all_channels)} قناة")
for k,v in groups.items(): print(f"{k}: {len(v)}")

def write_m3u(fname, lst):
    with open(fname,'w',encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for info,stream in lst: f.write(f"{info}\n{stream}\n")

# ta.m3u = الكل مصنف
write_m3u('ta.m3u', [(i,s) for i,s,l,c in all_channels])

# ملفات حسب اللغة - كل واحد مصنف داخلو
for lang_code, lang_name in [("AR","arabic-working"),("FR","France"),("IT","Italie"),("ES","Espagne"),("DE","Allemagne"),("UK","Angleterre"),("PT","Portugal"),("NL","Hollande")]:
    lst = [(i,s) for i,s,l,c in all_channels if l==lang_code]
    write_m3u(f'{lang_name}.m3u', lst)
    print(f"{lang_name}.m3u = {len(lst)}")

# ملفات حسب المغرب و المشرق للعربي
maghreb = [(i,s) for i,s,l,c in all_channels if l=="AR" and any(k in (i+s).lower() for k in ['alger','maroc','tunis','libya','mauritania'])]
mashreq = [(i,s) for i,s,l,c in all_channels if l=="AR" and (i,s) not in maghreb]
write_m3u('arabic-maghreb.m3u', maghreb)
write_m3u('arabic-mashreq.m3u', mashreq)
print(f"مغرب {len(maghreb)} مشرق {len(mashreq)}")
print("كمل")
