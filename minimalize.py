from pathlib import Path
import re
def gray(m):
 s=m.group(1)
 if len(s) not in (3,4,6,8):return m.group(0)
 if len(s) in (3,4):s=''.join(c*2 for c in s)
 rgb=[int(s[i:i+2],16) for i in (0,2,4)]
 n=round(.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2])
 return '#'+f'{n:02x}'*3+s[6:]
for name in ['style.css','redesign.css','app.js','scenes.js']:
 p=Path('dist')/name;s=p.read_text(encoding='utf-8');s=re.sub(r'#([0-9a-fA-F]{3,8})(?![0-9a-fA-F])',gray,s)
 s=s.replace('rgba(108,151,255,','rgba(186,186,186,').replace('rgba(137,229,255,','rgba(238,238,238,').replace('rgba(97,221,255,','rgba(220,220,220,')
 p.write_text(s,encoding='utf-8')
p=Path('dist/redesign.css')
with p.open('a',encoding='utf-8') as f:f.write('''
/* Solid, monochrome presentation. */
:root{--bg:#101010;--panel:#191919;--text:#f4f4f4;--muted:#aaa;--line:#333;--green:#e6e6e6;--phase:#ddd;--violet:#bbb}
body{background:#101010}header{background:#101010;backdrop-filter:none;-webkit-backdrop-filter:none}
.hero-visual,.hero-copy{background:none}.hero-grid{opacity:.35}
.hero h1 .serif{background:none;color:#c8c8c8;-webkit-text-fill-color:#c8c8c8}.serif{color:#c8c8c8}
.primary,.primary:hover{background:#f1f1f1;color:#111;box-shadow:none}.button{border-radius:0}
.hero-visual,#network{filter:none}.stack-strip,.lab-section,.results-section,.cinema-section{background:#151515}
.scenario-detail,.research-card,.telemetry,.chart-panel,.split-panel{background:#1b1b1b}
.lab,.film-frame,.paper-sheet,.primary,.meter i{box-shadow:none}.film-frame,.lab,.scenario-detail,.research-card,.chart-panel,.split-panel{border-radius:0;border-color:#383838}
.film-header,.film-footer,.scene-toolbar button{background:#202020}.film-header i{background:#ddd}
.scenario-list button.active{background:#242424;border-color:#eee}.scenario-list button:hover{background:#202020}
.chart-row.best .chart-bar{background:#e4e4e4}.chart-bar{background:#777}.paper-sheet{background:#e7e7e7;color:#151515}
.motion-button{background:#222;backdrop-filter:none;-webkit-backdrop-filter:none;border-color:#555;border-radius:2px}
.status-dot{background:#ddd;box-shadow:none}.segmented button.active{background:#ddd;color:#111}.topology-buttons button.active{background:#333;color:#eee}
.scene-legend i{background:#eee}.scene-legend span:nth-child(2) i{background:#999}
video{filter:grayscale(1)}.research-note>span{color:#ddd}
''')
