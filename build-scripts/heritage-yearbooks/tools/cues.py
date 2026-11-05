import re,sys
f,a,b=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
for blk in open(f).read().split("\n\n"):
    m=re.search(r"(\d+):(\d+):([\d.]+) --> (\d+):(\d+):([\d.]+)",blk)
    if not m: continue
    s=int(m[1])*3600+int(m[2])*60+float(m[3]); e=int(m[4])*3600+int(m[5])*60+float(m[6])
    if a<=s<=b: print(f"{s:8.2f}-{e:8.2f} "+" ".join(blk.split("\n")[1:]))
