from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,wave,subprocess,shutil,math,array,textwrap

ROOT=Path(__file__).parent
WORK=ROOT/'.narration-work';DIST=ROOT/'dist'
story=json.loads((ROOT/'narration-story.json').read_text(encoding='utf-8'))
parts=[];chapters=[];cues=[];cursor=0.0;audio_format=None
for index,scene in enumerate(story):
 start=cursor
 for j,sentence in enumerate(scene['sentences']):
  with wave.open(str(WORK/f'{index:02}-{j:02}.wav'),'rb') as f:
   fmt=(f.getnchannels(),f.getsampwidth(),f.getframerate());blob=f.readframes(f.getnframes())
  if audio_format is None:audio_format=fmt
  assert audio_format==fmt
  seconds=len(blob)/(fmt[0]*fmt[1]*fmt[2]);parts.append(blob)
  cues.append({'start':cursor,'end':cursor+seconds,'text':sentence,'scene':index})
  cursor+=seconds;gap=.28;parts.append(bytes(round(fmt[2]*gap)*fmt[0]*fmt[1]));cursor+=gap
 parts.append(bytes(round(fmt[2]*.6)*fmt[0]*fmt[1]));cursor+=.6
 chapters.append({'title':scene['title'],'start':round(start,3),'end':round(cursor,3),'tag':scene['tag'],'sentences':scene['sentences']})
with wave.open(str(WORK/'narration.wav'),'wb') as f:
 f.setnchannels(audio_format[0]);f.setsampwidth(audio_format[1]);f.setframerate(audio_format[2]);f.writeframes(b''.join(parts))
assert max(abs(x) for x in array.array('h',b''.join(parts)))>1000
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
(DIST/'narration-en.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(cues))+'\n',encoding='utf-8')
(DIST/'film-chapters.json').write_text(json.dumps({'duration':cursor,'voice':'Microsoft Zira Desktop','language':'English','chapters':chapters,'captions':'Burned-in English captions; WebVTT available for download.'}),encoding='utf-8')
(DIST/'narration-transcript.txt').write_text('BEYOND STATIC TRAFFIC\nEnglish narrated research explainer\nIllustrative animation, not experimental footage.\n\n'+'\n\n'.join(f"{stamp(c['start'])[:8]}  {c['title']}\n"+' '.join(c['sentences']) for c in chapters),encoding='utf-8')
W,H,FPS=1280,720,20
def font(size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
fonts={n:font(n) for n in [13,15,17,19,22,24,28,32,44,58]};bolds={n:font(n,True) for n in [17,22,28,44,58]}
def wrap(d,text,f,maxwidth):
 lines=[];line=''
 for word in text.split():
  test=(line+' '+word).strip()
  if d.textlength(test,font=f)>maxwidth and line:lines.append(line);line=word
  else:line=test
 if line:lines.append(line)
 return lines
def text(d,pos,s,size=19,color='#c8c8c4',bold=False):d.text(pos,str(s),font=bolds[size] if bold else fonts[size],fill=color)
def box(d,x,y,label,width=145):
 d.rounded_rectangle((x-width/2,y-29,x+width/2,y+29),radius=5,fill='#202020',outline='#a0a09a',width=2)
 text(d,(x-d.textlength(label,font=fonts[15])/2,y-9),label,15,'#eee')
def packets(d,a,b,t,count=5,reverse=False,color='#e6e6df'):
 d.line([a,b],fill='#565651',width=2)
 for k in range(count):
  u=(t/2.4+k/count)%1
  if reverse and k%2:u=1-u
  x=a[0]+(b[0]-a[0])*u;y=a[1]+(b[1]-a[1])*u
  d.rectangle((x-3,y-3,x+3,y+3),fill=color)
def network(d,t,kind):
 cy=352;source=(170,cy);switch=(540,cy);target=(940,cy)
 box(d,*source,'SOURCE HOST');box(d,*switch,'OPEN VSWITCH')
 if kind!='probe':box(d,*target,'TEST SERVICE')
 count=18 if kind=='udp' else 9 if kind=='benign' and math.sin(t)>0 else 1 if kind=='lowrate' else 5
 packets(d,(245,cy),(465,cy),t,count,kind=='churn')
 if kind=='probe':
  for j,off in enumerate([-96,-32,32,96]):
   end=(1045,cy+off);packets(d,(615,cy),(end[0]-35,end[1]),t+j*.5,2)
   box(d,*end,f'PORT {j+1}',95)
 else:packets(d,(615,cy),(865,cy),t,count,kind=='churn')
 descriptions={'probe':'BOUNDED PORT RANGE','udp':'CONTROLLED TRAFFIC INCREASE','churn':'ESTABLISH > TEAR DOWN > REPEAT','lowrate':'SPARSE PROBES / CONTROLLED SERVICE','benign':'BASELINE + AUTHORIZED BURSTS'}
 text(d,(70,476),descriptions[kind],17,'#b6b6b0')
def panel(d,x,y,w,h,title):
 d.rectangle((x,y,x+w,y+h),fill='#191919',outline='#4a4a46',width=1);text(d,(x+20,y+18),title,17,'#c0c0b9')
def draw_visual(d,scene,t,local):
 kind=scene['kind'];p=min(1,local/1.2)
 if kind in ['benign','probe','udp','churn','lowrate']:network(d,t,kind)
 elif kind in ['intro','stack']:
  box(d,640,250,'RYU CONTROLLER',200)
  for i,x in enumerate([330,640,950]):
   packets(d,(640,280),(x,350),t+i,3,color='#9cc9dc');box(d,x,370,'OVS '+str(i+1),140)
   for xx in [x-65,x+65]:packets(d,(x,400),(xx,465),t+i,2);box(d,xx,480,'HOST',90)
  text(d,(65,224),'CONTROL PLANE',15,'#92928a');text(d,(65,362),'DATA PLANE',15,'#92928a')
 elif kind=='phases':
  phase=int(local/4)%3
  for i,(name,desc) in enumerate([('STABLE','Reference conditions'),('CONSTRAINED','Controlled settings change'),('RECOVERY','Reference restored')]):
   x=65+i*395;panel(d,x,260,365,195,name)
   for j,line in enumerate(wrap(d,desc,fonts[22],310)):text(d,(x+20,320+j*30),line,22,'#eee' if i==phase else '#888')
   if i==phase:d.rectangle((x,453,x+365,458),fill='#eee')
   if i<2:text(d,(x+370,345),'>',22,'#ddd')
  text(d,(65,490),'PHASE EVENTS PRESERVE TIMING CONTEXT',17,'#b0b0a8')
 elif kind=='telemetry':
  labels=['FLOW COUNTERS','RTT SAMPLES','UDP MEASUREMENTS','EVENT TIMESTAMPS']
  for i,label in enumerate(labels):
   y=232+i*68;box(d,240,y,label,270);packets(d,(375,y),(690,345),t+i,3)
  box(d,855,345,'OBSERVATION WINDOW',300);text(d,(705,412),'run_id + features + context',19,'#b0b0a8')
 elif kind=='labels':
  colors=['#809aaa','#b8a98a','#95aa92']
  for i,label in enumerate(['STABLE','CONSTRAINED','RECOVERY']):
   x=70+i*380;d.rectangle((x,254,x+370,315),fill=colors[i]);text(d,(x+20,272),label,19,'#111')
  x=70+(t*45)%1050;d.rectangle((x,240,x+85,335),outline='#fff',width=3)
  for i,(a,b) in enumerate([('PHASE','Verified network events'),('ACTIVITY','Recorded workload intervals'),('QUALITY','Observed / transition / partial')]):text(d,(75,375+i*45),a,17,'#aaa');text(d,(280,371+i*45),b,24,'#eee')
 elif kind=='dataset':
  for i,(name,shade) in enumerate([('TRAIN','#8e8e89'),('VALIDATION','#adada6'),('TEST','#d9d9d0')]):
   x=70+i*395;panel(d,x,242,365,240,name);text(d,(x+25,292),'72',58,'#eee',True);text(d,(x+25,375),'observations / 8 runs',22,'#b2b2a9');d.rectangle((x+25,432,x+25+int(315*p),442),fill=shade)
  text(d,(70,509),'NO SHARED RUN IDs BETWEEN PARTITIONS',17,'#bbb')
 elif kind=='models':
  names=['Logistic Regression','Random Forest','RBF-SVM','Gradient Boosting','Soft Voting Ensemble'];values=[62.5,88.75,50,89.58,87.5];colors=['#4ea5ed','#51c7a4','#e6b254','#a68bf0','#ec859c']
  for i,(name,v,color) in enumerate(zip(names,values,colors)):
   y=230+i*53;text(d,(65,y),name,19,'#c9c9c2');d.rectangle((360,y+4,1100,y+24),fill='#242424');d.rectangle((360,y+4,360+int(740*v/100*p),y+24),fill=color);text(d,(1120,y),f'{v:.2f}%',19,'#eee')
  text(d,(65,509),'BALANCED ACCURACY / TABLE IV / SYNTHETIC PROBING',15,'#aaa')
 elif kind=='fidelity':
  names=['Stable','Constrained','Recovery'];rtt=[6.0508,32.8780,6.2758];gp=[9.2999,1.9001,9.2628]
  for k,(title,values,maximum,unit) in enumerate([('Mean RTT',rtt,40,'ms'),('TCP bulk goodput',gp,10,'Mbps')]):
   x=65+k*620;text(d,(x,219),title,24,'#eee')
   for i,(name,v) in enumerate(zip(names,values)):
    y=285+i*65;text(d,(x,y),name,17,'#aaa');d.rectangle((x+135,y+5,x+135+int(295*v/maximum*p),y+25),fill=['#9ab9ca','#dfb47e','#a9c3a0'][i]);text(d,(x+450,y),f'{v:.4f}',17,'#eee')
   text(d,(x,502),unit.upper()+' / REPORTED PHASE MEANS',15,'#aaa')
 elif kind=='limits':
  panel(d,65,245,550,255,'SUPPORTED IN THE REPORTED LAB SCOPE');panel(d,655,245,560,255,'NOT YET ESTABLISHED')
  for i,line in enumerate(['Controlled SDN traffic generation','Traceable dataset construction','Synthetic-workload evaluation','Measured phase response']):text(d,(90,305+i*42),line,22,'#ddd')
  for i,line in enumerate(['Independent malicious ground truth','Unseen attack-family generalization','Production-network effectiveness']):text(d,(680,315+i*50),line,22,'#aaa')

out=WORK/'narrated-picture.mp4'
proc=subprocess.Popen([shutil.which('ffmpeg'),'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
scene_index=cue_index=0;frame_count=math.ceil(cursor*FPS)
for frame in range(frame_count):
 t=frame/FPS
 while scene_index+1<len(chapters) and t>=chapters[scene_index]['end']:scene_index+=1
 while cue_index+1<len(cues) and t>=cues[cue_index]['end']:cue_index+=1
 scene=story[scene_index];chapter=chapters[scene_index];local=t-chapter['start']
 im=Image.new('RGB',(W,H),'#101010');d=ImageDraw.Draw(im)
 text(d,(65,35),'PHASE / FLOW',17,'#e0e0d8',True);text(d,(875,38),'ENGLISH NARRATION / RESEARCH EXPLAINER',13,'#85857e')
 d.line((65,75,1215,75),fill='#3b3b37',width=1);text(d,(65,105),scene['title'],44,'#f2f2e9',True);text(d,(67,167),scene['tag'],15,'#9b9b93')
 draw_visual(d,scene,t,local)
 d.rectangle((45,555,1235,663),fill='#1e1e1c')
 cue=cues[cue_index]
 if cue['start']<=t<=cue['end']:
  lines=wrap(d,cue['text'],fonts[24],1120)
  for j,line in enumerate(lines[:3]):text(d,(75,572+j*29),line,24,'#efefe7')
 text(d,(65,680),'ILLUSTRATIVE ANIMATION / NOT RECORDED EXPERIMENTAL FOOTAGE',13,'#777770');text(d,(1090,680),f'{scene_index+1:02} / {len(story):02}',13,'#bbb')
 d.rectangle((0,H-3,round(W*t/cursor),H),fill='#d8d8d0')
 if frame==30:im.save(DIST/'film-poster-narrated.jpg',quality=94)
 if scene_index in [4,11,12] and abs(local-2)<1/FPS:im.save(WORK/f'preview-{scene_index}.jpg',quality=92)
 proc.stdin.write(im.tobytes())
 if frame%(FPS*30)==0:print(f'Rendered {t:.0f} / {cursor:.0f} seconds',flush=True)
proc.stdin.close()
assert proc.wait()==0
subprocess.run([shutil.which('ffmpeg'),'-y','-i',str(out),'-i',str(WORK/'narration.wav'),'-c:v','copy','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(DIST/'research-explainer-english.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print(f'COMPLETE: {cursor:.2f} seconds, 14 chapters, English speech + burned-in captions.',flush=True)
