from PIL import Image,ImageDraw,ImageFont
import math,subprocess,shutil
from pathlib import Path
W,H,FPS=960,540,24
def font(size,bold=False):
 return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
fsmall,font18,ftitle,fnode=font(12),font(18),font(36,True),font(14,True)
scenes=[('01','Bounded TCP probing','A01 / Synthetic workload','Multiple ports. One controlled testbed.','Generator-side evidence does not establish attack success.'),('02','Controlled UDP increase','A02 / Synthetic workload','More packets. Explicit workload context.','Higher traffic intensity alone is not a malicious ground truth.'),('03','TCP connection churn','A03 / Synthetic workload','Connect. Tear down. Repeat.','Endpoint-level verification; independent adjudication incomplete.'),('04','Low-rate service probing','A04 / Synthetic workload','Sparse signals against a controlled service.','Synthetic probing is not validation of unseen malicious attacks.')]
out=Path('dist/traffic-explainer.mp4')
proc=subprocess.Popen([shutil.which('ffmpeg'),'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
for frame in range(24*FPS):
 t=frame/FPS;si=min(int(t//6),3);local=t%6;num,title,category,desc,note=scenes[si]
 im=Image.new('RGB',(W,H),'#090d20');d=ImageDraw.Draw(im)
 for x in range(0,W,40):d.line((x,0,x,H),fill='#131b34')
 for y in range(0,H,40):d.line((0,y,W,y),fill='#131b34')
 d.ellipse((630,-190,1140,320),fill='#101733');d.text((36,28),'PHASE / FLOW',font=fnode,fill='#72dfff');d.text((660,30),'PAPER-BASED VISUAL EXPLAINER',font=fsmall,fill='#a4b6d9')
 d.text((36,75),title,font=ftitle,fill='#f0f3ff');d.text((37,126),category.upper(),font=fsmall,fill='#c3a4ff');d.text((37,154),desc,font=font18,fill='#a5b9de')
 cy=310;sx,mx,tx=115,460,820;purple='#c1a0ff';cyan='#68dfff';lanes=[-62,-21,21,62] if si==0 else [0]
 for lane in lanes:d.line([(sx+40,cy),(mx,cy),(tx-35,cy+lane)],fill='#39476d',width=2)
 count=[10,48,12,2][si]
 for j in range(count):
  q=(local/([2.3,1.6,1.9,4][si])+j/count)%1
  if si==2 and j%2:q=1-q
  lane=lanes[j%len(lanes)];x=sx+40+(tx-sx-75)*q;y=cy+(max(0,q-.5)*2*lane)+(j%5-2)*4*(si==1);color=cyan if si==2 and j%2 else purple
  d.ellipse((x-8,y-8,x+8,y+8),fill='#222c52');d.ellipse((x-3,y-3,x+3,y+3),fill=color)
 for i,(x,label) in enumerate([(sx,'SOURCE HOST'),(mx,'OPEN VSWITCH'),(tx,'TEST SERVICE')]):
  if si==0 and i==2:
   for j,lane in enumerate(lanes):d.rounded_rectangle((x-33,cy+lane-15,x+33,cy+lane+15),radius=5,fill='#18213c',outline=purple,width=1);d.text((x-22,cy+lane-7),f'PORT {j+1}',font=fsmall,fill='#d5d9f1')
  else:
   d.rounded_rectangle((x-40,cy-33,x+40,cy+33),radius=10,fill='#182440',outline=cyan if i==1 else purple,width=2)
   for row in range(3):d.line((x-20,cy-12+row*12,x+20,cy-12+row*12),fill=cyan if i==1 else purple,width=2)
  d.text((x-d.textlength(label,font=fsmall)/2,cy+88),label,font=fsmall,fill='#a7bbde')
 if si==2:d.text((345,238),'CONNECT  /  CLOSE  /  REPEAT',font=fsmall,fill=cyan)
 if si==3:d.text((365,250),'LOW-RATE PROBES',font=fsmall,fill=purple)
 d.line((36,439,924,439),fill='#303e61',width=1);d.text((36,460),note,font=font18,fill='#c1cce5');d.text((36,505),'ILLUSTRATIVE ANIMATION / NOT EXPERIMENTAL FOOTAGE',font=fsmall,fill='#8497be');d.text((835,505),num+' / 04',font=fsmall,fill=cyan)
 d.rectangle((0,H-3,int(W*frame/(24*FPS-1)),H),fill=cyan)
 if frame==35:im.save('dist/film-poster.jpg',quality=93)
 proc.stdin.write(im.tobytes())
proc.stdin.close()
if proc.wait()!=0:raise RuntimeError('Video encoding failed')
print(f'Created {out}: {out.stat().st_size} bytes, 24 seconds')
