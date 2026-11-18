(() => {
  const video=document.querySelector('#research-film');
  const list=document.querySelector('#film-chapter-list');
  const transcript=document.querySelector('#film-transcript');
  const clock=t=>`${Math.floor(t/60)}:${String(Math.floor(t%60)).padStart(2,'0')}`;
  let chapters=[],current=-1,chapterRequest=0,seekableCopy=null,copyReady=null;
  const originalMediaURL=new URL(video.querySelector('source').getAttribute('src'),document.baseURI).href;
  const note=document.querySelector('#film-audio-note');
  // Some static hosts return MP4 files without usable byte-range seeking.
  // A complete local Blob is seekable independently of the host's range support.
  function prepareSeekableCopy(){
    if(copyReady)return copyReady;
    copyReady=(async()=>{
      const response=await fetch(originalMediaURL,{credentials:'same-origin'});
      if(!response.ok)throw new Error('The video could not be downloaded.');
      const bytes=await response.arrayBuffer();
      if(!bytes.byteLength)throw new Error('The downloaded video is empty.');
      seekableCopy=URL.createObjectURL(new Blob([bytes],{type:'video/mp4'}));
      await new Promise((resolve,reject)=>{
        const cleanup=()=>{clearTimeout(timer);video.removeEventListener('loadedmetadata',loaded);video.removeEventListener('error',failed);};
        const loaded=()=>{cleanup();resolve();};
        const failed=()=>{cleanup();reject(new Error('The seekable video could not be opened.'));};
        const timer=setTimeout(failed,15000);
        video.addEventListener('loadedmetadata',loaded);
        video.addEventListener('error',failed);
        video.src=seekableCopy;
        video.load();
      });
    })().catch(error=>{copyReady=null;if(seekableCopy){URL.revokeObjectURL(seekableCopy);seekableCopy=null;}throw error;});
    return copyReady;
  }
  function seekTo(seconds){
    const target=Math.min(seconds+.04,Math.max(0,video.duration-.05));
    if(Math.abs(video.currentTime-target)<.02)return Promise.resolve();
    return new Promise((resolve,reject)=>{
      const cleanup=()=>{clearTimeout(timer);video.removeEventListener('seeked',done);video.removeEventListener('error',failed);};
      const done=()=>{cleanup();resolve();};
      const failed=()=>{cleanup();reject(new Error('The selected chapter could not be opened.'));};
      const timer=setTimeout(failed,10000);
      video.addEventListener('seeked',done);
      video.addEventListener('error',failed);
      video.currentTime=target;
    });
  }
  async function selectChapter(index){
    const chapter=chapters[index];if(!chapter)return;
    const request=++chapterRequest;
    video.pause();list.setAttribute('aria-busy','true');
    note.textContent=`Preparing chapter ${index+1}: ${chapter.title}. The video loads once for reliable chapter navigation.`;
    try{
      await prepareSeekableCopy();
      if(request!==chapterRequest||!video.closest('section').classList.contains('route-active'))return;
      await seekTo(chapter.start);
      if(request!==chapterRequest||!video.closest('section').classList.contains('route-active'))return;
      updateChapter();
      await video.play().catch(()=>{note.textContent='Chapter selected. Press Play on the video to hear the English narration.';});
    }catch(error){if(request===chapterRequest)note.textContent='Unable to load that chapter. Select it again to retry, or use Download narrated video below.';}
    finally{if(request===chapterRequest)list.removeAttribute('aria-busy');}
  }
  fetch('film-chapters.json').then(r=>{if(!r.ok)throw Error('Chapter information unavailable');return r.json();}).then(data=>{
    chapters=data.chapters;document.querySelector('#film-duration').textContent=`${clock(data.duration)} / 14 CHAPTERS / ENGLISH VOICE`;
    document.querySelectorAll('[data-film-duration]').forEach(el=>el.textContent=clock(data.duration));
    list.replaceChildren();transcript.replaceChildren();
    chapters.forEach((chapter,index)=>{
      const button=document.createElement('button');button.className='film-chapter';button.type='button';button.setAttribute('aria-label',`Play chapter ${index+1}: ${chapter.title}`);
      const time=document.createElement('span');time.textContent=clock(chapter.start);const title=document.createElement('strong');title.textContent=chapter.title;
      button.append(time,title);button.addEventListener('click',()=>selectChapter(index));list.append(button);
      const article=document.createElement('article'),heading=document.createElement('h3'),seek=document.createElement('button'),p=document.createElement('p');
      seek.type='button';seek.textContent=`${clock(chapter.start)} · ${chapter.title}`;seek.addEventListener('click',()=>{selectChapter(index);video.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});});heading.append(seek);p.textContent=chapter.sentences.join(' ');article.append(heading,p);transcript.append(article);
    });
    updateChapter();
  }).catch(()=>{list.textContent='Chapter list could not load. Use the video timeline or download the transcript below.';});
  function updateChapter(){const index=chapters.findIndex(c=>video.currentTime>=c.start&&video.currentTime<c.end);if(index===current)return;current=index;list.querySelectorAll('button').forEach((button,i)=>{if(i===index)button.setAttribute('aria-current','true');else button.removeAttribute('aria-current');});document.querySelector('#film-now-playing').textContent=index>=0?`${index+1} / ${chapters.length} · ${chapters[index].title}`:'English narrated research explainer';}
  video.addEventListener('timeupdate',updateChapter);
  video.addEventListener('play',()=>{document.querySelector('#film-audio-note').textContent=video.muted?'Audio is muted. Use the speaker control to hear the English narration.':'Playing English narration · Captions are included in the picture.';});
  video.addEventListener('volumechange',()=>{document.querySelector('#film-audio-note').textContent=video.muted||video.volume===0?'Audio is muted. Use the speaker control to hear the English narration.':'English narration enabled · Captions are included in the picture.';});
})();
