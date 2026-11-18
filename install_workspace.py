from pathlib import Path
p=Path('dist/index.html');s=p.read_text(encoding='utf-8')
start=s.index('<section class="hero"');end=s.index('<div class="stack-strip">',start)
s=s[:start]+Path('workspace-hero.html').read_text(encoding='utf-8')+s[end:]
start=s.index('<nav aria-label="Main navigation">');end=s.index('</nav>',start)+6
s=s[:start]+'''<nav aria-label="Main navigation"><a href="#home">Network lab</a><a href="#results">Results</a><a href="#dataset">Dataset</a><a href="#gallery">Graphs</a><a href="#research">Research</a><a href="#downloads" class="download-nav">Downloads ↓</a></nav>'''+s[end:]
s=s.replace('<script src="evidence.js" defer></script>','<script src="evidence.js" defer></script><script src="workspace.js" defer></script>')
s=s.replace('<link rel="stylesheet" href="evidence.css">','<link rel="stylesheet" href="evidence.css"><link rel="stylesheet" href="workspace.css">')
s=s.replace('An interactive showcase of the supplied capstone research.','Mininet · Ryu · Open vSwitch · OpenFlow 1.3')
s=s.replace('<a href="#home">Back to top ↑</a>','<a href="#home">Return to the network lab ↗</a>')
p.write_text(s,encoding='utf-8')
p=Path('dist/workspace.css');s=p.read_text(encoding='utf-8').replace('grid-template-columns:205px minmax(0,1fr))','grid-template-columns:205px minmax(0,1fr)')
s+='\n.node-accessible{position:absolute;z-index:5;left:20px;top:20px;display:flex;gap:5px}.node-accessible button{position:absolute;width:1px;height:1px;padding:0;overflow:hidden;clip-path:inset(50%);border:0}.node-accessible button:focus{position:relative;width:auto;height:auto;padding:10px;clip-path:none;background:#eee;color:#111;border:1px solid #777}.research-extras{display:flex;flex-wrap:wrap;gap:25px;font-size:11px;margin-bottom:35px}.research-extras a{text-decoration:underline;text-underline-offset:5px}.workspace-intro-right .watch-film:focus-visible,.network-workspace button:focus-visible{outline:2px solid currentColor;outline-offset:3px}\n'
p.write_text(s,encoding='utf-8')
