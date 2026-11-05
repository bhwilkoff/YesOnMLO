# usage: strip.py src t0 t1 step out.jpg  -> contact sheet with timestamps
import subprocess,sys
from PIL import Image,ImageDraw
src,t0,t1,step,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
ts=[];t=t0
while t<=t1: ts.append(t);t+=step
ims=[]
for t in ts:
    raw=subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.2f}","-i",src,"-frames:v","1","-vf","scale=320:240","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    im=Image.frombytes("RGB",(320,240),raw);ImageDraw.Draw(im).text((6,6),f"{t:.1f}",fill="yellow");ims.append(im)
cols=6;rows=(len(ims)+cols-1)//cols
s=Image.new("RGB",(320*cols,240*rows))
for i,im in enumerate(ims): s.paste(im,((i%cols)*320,(i//cols)*240))
s.save(out)
