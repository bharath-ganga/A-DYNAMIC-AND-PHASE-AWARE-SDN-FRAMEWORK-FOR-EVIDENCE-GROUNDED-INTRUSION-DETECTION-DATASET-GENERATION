"""Local static preview with HTTP byte ranges for narrated-video seeking."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import os,re

class Handler(SimpleHTTPRequestHandler):
 def end_headers(self):
  self.send_header('Accept-Ranges','bytes');super().end_headers()
 def __init__(self,*a,**k):super().__init__(*a,directory=str(Path(__file__).parent/'dist'),**k)
 def send_head(self):
  self.remaining=None
  path=self.translate_path(self.path)
  header=self.headers.get('Range','')
  if not header or not os.path.isfile(path):return super().send_head()
  match=re.fullmatch(r'bytes=(\d+)-(\d*)',header)
  if not match:return super().send_head()
  f=open(path,'rb');size=os.fstat(f.fileno()).st_size;start=int(match[1]);end=min(int(match[2]) if match[2] else size-1,size-1)
  if start>=size or end<start:
   f.close();self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();return None
  self.send_response(206);self.send_header('Content-type',self.guess_type(path));self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(end-start+1));self.end_headers();f.seek(start);self.remaining=end-start+1;return f
 def copyfile(self,source,outputfile):
  if self.remaining is None:return super().copyfile(source,outputfile)
  left=self.remaining
  try:
   while left:
    block=source.read(min(left,65536))
    if not block:break
    outputfile.write(block);left-=len(block)
  except (BrokenPipeError,ConnectionResetError):pass

print('Preview: http://localhost:4173',flush=True)
ThreadingHTTPServer(('127.0.0.1',4173),Handler).serve_forever()
