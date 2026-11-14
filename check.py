import requests, re, concurrent.futures

urls=[]
for fname in ['servers-all.txt','servers-backup.txt']:
    try:
        with open(fname,encoding='utf-8',errors='ignore') as f:
            for l in f:
                l=l.strip()
                if l.startswith('http'): urls.append(l)
    except: pass

arabic={}; french={}; italian={}; spanish={}; german={}; english={}; portuguese={}; dutch={}

def is_arabic(info,url):
    low=(info+" "+url).lower()
    return any(w in low for w in ['ara','arab','alger','dz','maroc','ma,','tunis','tn','egypt','eg','saudi','sa','mbc','jazeera','maghreb','mashreq','bein','ssc','qatar','kuwait','iraq','jordan','lebanon','syria','yemen','oman','bahrain','libya','sudan','mauritania','palestine'])
def is_french(info,url):
    low=(info+" "+url).lower()
    return any(w in low for w in ['fra','french','france','fr,','tf1','france 2','france 3','france 5','france 24','m6','c8','bfm','lci','arte','canal+','rmc','tnt','paris','lequipe','cnews','tv5','gulli','w9'])
def is_italian(info,url):
    low=(info+" "+url).lower()
    return any(w in low for w in ['ita','italy','italia','it,','rai 1','rai 2','rai 3','canale 5','italia 1','rete 4','la7','mediaset','sky italia','tv8','nove'])
def is_spanish(info,url):
    low=(info+" "+url).lower()
    return any(w in low for w in ['spa','spain','espa','es,','la 1','la 2','antena 3','telecinco','cuatro','la sexta','tve','movistar','dazn es','real madrid tv','barca tv','gol tv','canal sur'])
def is_german(info,url):
    low=(info+" "+url).lower()
    return any(w in low for w in ['ger','germany','deutschland','de,','ard','zdf','rtl','pro7','pro 7','sat.1','sat1','vox','kabel eins','sky de','dazn de','sport1','ntv','n-tv'])
def is_english(info,url):
    low=(info+" "+url).lower()
    return any(w in low for w in ['uk','england','british','bbc','itv','channel 4','channel 5','sky sports','sky uk','sky news','dazn uk','bt sport','tnt sports uk','eurosport uk'])
def is_portuguese(info,url):
    low=(info+" "+url).lower()
    return any(w in low for w in ['por','portugal','pt,','rtp','sic','tvi','sport tv','benfica tv','porto canal','cnn portugal'])
def is_dutch(info,url):
    low=(info+" "+url).lower()
    return any(w in low for w in ['nld','netherlands','holland','nl,','npo 1','npo 2','npo 3','rtl 4','rtl 5','rtl 7','ziggo','sbs 6','veronica','espn nl'])

for surl in urls:
    try:
        r=requests.get(surl,timeout=30,headers={'User-Agent':'Mozilla/5.0'})
        parts=re.split(r'(?=#EXTINF)',r.text)
        for p in parts:
            if '#EXTINF' not in p: continue
            lines=p.strip().splitlines()
            if len(lines)<2: continue
            info=lines[0]; stream=lines[1].strip()
            if not stream.startswith('http'): continue
            m=re.search(r',(.+)$',info); name=m.group(1).strip() if m else stream
            if is_arabic(info,stream) and name not in arabic: arabic[name]=(info,stream)
            if is_french(info,stream) and name not in french: french[name]=(info,stream)
            if is_italian(info,stream) and name not in italian: italian[name]=(info,stream)
            if is_spanish(info,stream) and name not in spanish: spanish[name]=(info,stream)
            if is_german(info,stream) and name not in german: german[name]=(info,stream)
            if is_english(info,stream) and name not in english: english[name]=(info,stream)
            if is_portuguese(info,stream) and name not in portuguese: portuguese[name]=(info,stream)
            if is_dutch(info,stream) and name not in dutch: dutch[name]=(info,stream)
    except Exception as e: print(f"فشل {surl}: {e}")

def is_working(item):
    name,(info,stream)=item
    try:
        r=requests.head(stream,timeout=8,allow_redirects=True,headers={'User-Agent':'Mozilla/5.0'})
        if r.status_code<400: return item
        r2=requests.get(stream,timeout=8,stream=True,headers={'User-Agent':'Mozilla/5.0','Range':'bytes=0-1000'})
        if r2.status_code<400: return item
    except: pass
    return None

def check_all(d):
    out=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
        for res in ex.map(is_working,list(d.items())):
            if res: out.append(res)
    return out

aw=check_all(arabic); fw=check_all(french); iw=check_all(italian); sw=check_all(spanish); gw=check_all(german); ew=check_all(english); pw=check_all(portuguese); dw=check_all(dutch)
print(f"عربي {len(aw)} فرنسي {len(fw)} إيطالي {len(iw)} إسباني {len(sw)} ألماني {len(gw)} إنجليزي {len(ew)} برتغالي {len(pw)} هولندي {len(dw)}")

def write_m3u(fname,lst):
    with open(fname,'w',encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for info,stream in lst: f.write(f"{info}\n{stream}\n")

maghreb=[]; mashreq=[]
for name,(info,stream) in aw:
    low=(name+" "+info).lower()
    if any(k in low for k in ['alger','dz','maroc','ma,','tunis','tn','libya','mauritania']): maghreb.append((info,stream))
    else: mashreq.append((info,stream))

write_m3u('arabic-working.m3u',aw); write_m3u('arabic-maghreb.m3u',maghreb); write_m3u('arabic-mashreq.m3u',mashreq)
write_m3u('France.m3u',fw); write_m3u('french-working.m3u',fw)
write_m3u('Italie.m3u',iw); write_m3u('italie.m3u',iw)
write_m3u('Espagne.m3u',sw); write_m3u('espagne.m3u',sw)
write_m3u('Allemagne.m3u',gw); write_m3u('allemagne.m3u',gw)
write_m3u('Angleterre.m3u',ew); write_m3u('angleterre.m3u',ew)
write_m3u('Portugal.m3u',pw); write_m3u('portugal.m3u',pw)
write_m3u('Hollande.m3u',dw); write_m3u('hollande.m3u',dw)
print("تم كلش")
