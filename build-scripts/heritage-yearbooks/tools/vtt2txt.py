import re,sys
txt=open(sys.argv[1]).read()
out=[];last=""
for blk in txt.split("\n\n"):
    m=re.search(r"(\d+):(\d+):(\d+)\.(\d+) -->",blk)
    if not m: continue
    t=int(m[1])*3600+int(m[2])*60+int(m[3])
    lines=[re.sub(r"<[^>]+>","",l).strip() for l in blk.split("\n")[1:] if "-->" not in l]
    lines=[l for l in lines if l]
    if not lines: continue
    cur=lines[-1]
    if cur!=last and cur not in last:
        out.append(f"{t//60:02d}:{t%60:02d} {cur}");last=cur
print("\n".join(out))
