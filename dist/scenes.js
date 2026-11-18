// Conceptual packet choreography only. No network traffic is generated.
const sceneCanvas=document.querySelector('#attack-scene');
const sceneCtx=sceneCanvas.getContext('2d');
let sceneWidth=0,sceneHeight=0,sceneTime=0,sceneLast=0,scenePlaying=true;
new ResizeObserver(()=>{const r=sceneCanvas.getBoundingClientRect();sceneWidth=r.width;sceneHeight=r.height;const d=Math.min(devicePixelRatio||1,2);sceneCanvas.width=r.width*d;sceneCanvas.height=r.height*d;sceneCtx.setTransform(d,0,0,d,0,0);}).observe(sceneCanvas);
document.querySelector('#scene-play').addEventListener('click',()=>{scenePlaying=!scenePlaying;document.querySelector('#scene-play').textContent=scenePlaying?'Ⅱ Pause scene':'▶ Play scene';document.querySelector('#scene-play').setAttribute('aria-pressed',scenePlaying);});
function sceneFrame(now){const delta=sceneLast?Math.min(now-sceneLast,50):0;sceneLast=now;if(scenePlaying&&!paused&&!document.hidden)sceneTime+=delta;renderScene();requestAnimationFrame(sceneFrame);}
function renderScene(){const c=sceneCtx,w=sceneWidth,h=sceneHeight;if(!w)return;c.clearRect(0,0,w,h);const selected=Number(document.querySelector('[data-scenario].active').dataset.scenario),synthetic=selected>1,color=synthetic?'#acacac':'#c5c5c5';const sx=w*.13,mx=w*.49,tx=w*.86,cy=h*.48;
 c.strokeStyle='#242424';c.lineWidth=.5;for(let i=20;i<w;i+=24){c.beginPath();c.moveTo(i,0);c.lineTo(i,h);c.stroke();}for(let i=20;i<h;i+=24){c.beginPath();c.moveTo(0,i);c.lineTo(w,i);c.stroke();}
 const lanes=selected===2?[-45,-15,15,45]:[0];
 lanes.forEach((offset,i)=>{c.strokeStyle='#434343';c.lineWidth=1;c.beginPath();c.moveTo(sx+22,cy);c.lineTo(mx,cy);c.lineTo(tx-22,cy+offset);c.stroke();if(selected===2){c.fillStyle='#aeaeae';c.font='7px monospace';c.fillText('PORT '+(i+1),tx-15,cy+offset+21);}});
 const count=selected===3?30:selected===1?18:selected===5?2:selected===4?9:7;
 for(let i=0;i<count;i++){const cycle=selected===5?4600:phase===1?3400:1900;let t=(sceneTime/cycle+i/count)%1;let back=selected===4&&i%2===1;if(back)t=1-t;const lane=lanes[i%lanes.length];const x=sx+22+(tx-sx-44)*t,y=cy+(t>.5?(t-.5)*2*lane:0)+(selected===3?(i%5-2)*4:0);c.fillStyle=selected===4&&back?'#c5c5c5':color;c.shadowColor=c.fillStyle;c.shadowBlur=8;c.beginPath();c.arc(x,y,selected===3?2:3,0,Math.PI*2);c.fill();c.shadowBlur=0;}
 [[sx,cy,'SOURCE'],[mx,cy,'OVS'],[tx,cy,'SERVICE']].forEach(([x,y,label],i)=>{if(selected===2&&i===2){lanes.forEach(off=>{c.fillStyle='#1c1c1c';c.strokeStyle=color;c.fillRect(x-12,y+off-10,24,20);c.strokeRect(x-12,y+off-10,24,20);});return;}c.fillStyle='#1e1e1e';c.strokeStyle=i===1?'#c5c5c5':color;c.lineWidth=1;c.beginPath();c.roundRect(x-22,y-20,44,40,6);c.fill();c.stroke();c.fillStyle='#d4d4d4';c.font='15px sans-serif';c.textAlign='center';c.fillText(i===1?'≋':'▱',x,y+5);c.font='7px monospace';c.fillStyle='#b3b3b3';c.fillText(label,x,y+36);});c.textAlign='left';c.font='8px monospace';c.fillStyle=color;const captions=['CONTINUOUS UDP + ICMP','AUTHORIZED BENIGN BURST','BOUNDED MULTI-PORT PROBING','CONTROLLED UDP INCREASE','CONNECT → TEAR DOWN → REPEAT','SPARSE PROBES / CONTROLLED SERVICE'];c.fillText(captions[selected],15,h-15);c.fillStyle='#9e9e9e';c.fillText('CONCEPT VIEW',15,20);
}
requestAnimationFrame(sceneFrame);
document.addEventListener('visibilitychange',()=>{if(document.hidden)document.querySelector('#research-film').pause();});
