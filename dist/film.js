(() => {
  const video=document.querySelector('#research-film');
  const list=document.querySelector('#film-chapter-list');
  const transcript=document.querySelector('#film-transcript');
  const clock=t=>`${Math.floor(t/60)}:${String(Math.floor(t%60)).padStart(2,'0')}`;
  let chapters=[],current=-1;
  function selectChapter(index){const chapter=chapters[index];if(!chapter)return;video.currentTime=chapter.start;video.play().catch(()=>{document.querySelector('#film-audio-note').textContent='Press Play on the video to start the English narration.';});}
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
