import argparse, json, os, shutil, subprocess, uuid
from pathlib import Path
from source_detector import detect_source
from ranking import Candidate, rank_candidates, score_candidate, refine_boundaries
from clipper import render_clip

def download(url, work):
    source=detect_source(url)
    if source not in ('youtube','twitch'): raise ValueError('Unsupported source. Use a YouTube or Twitch URL.')
    out=str(work/'source.%(ext)s')
    subprocess.run(['yt-dlp','--no-playlist','-f','bv*+ba/b','--merge-output-format','mp4','-o',out,url],check=True)
    files=list(work.glob('source.*')); return next((p for p in files if p.suffix not in ('.part','.json')),None)

def transcribe(audio):
    try:
        from faster_whisper import WhisperModel
        model=WhisperModel('tiny',device='cpu',compute_type='int8')
        segs,_=model.transcribe(str(audio),word_timestamps=True)
        return [{'start':s.start,'end':s.end,'text':s.text.strip()} for s in segs]
    except Exception as e:
        return [{'start':0,'end':30,'text':'Transcription unavailable in this environment. Install faster-whisper to enable local AI transcription.'}]

def process(url, clip_count=5, brief=''):
    job=Path('jobs')/uuid.uuid4().hex; job.mkdir(parents=True)
    source=download(url,job)
    wav=job/'audio.wav'; subprocess.run(['ffmpeg','-y','-i',str(source),'-ar','16000','-ac','1',str(wav)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    segments=transcribe(wav); json.dump({'segments':segments},open(job/'transcript.json','w'),indent=2)
    candidates=[]
    for s in segments:
        if len(s['text'].split())>=5:
            start,end=refine_boundaries(segments,s['start'],s['end']); score=score_candidate(s['text'],end-start,brief); candidates.append(Candidate(start,end,s['text'][:80], 'Standalone thought with strong hook potential','general',score))
    chosen=rank_candidates(candidates,clip_count); outputs=[]
    for i,c in enumerate(chosen,1):
        out=job/'output'/f'clip_{i:02d}.mp4'; render_clip(str(source),str(out),c.start,c.end,c.hook); outputs.append({'file':str(out),'start':c.start,'end':c.end,'hook':c.hook,'score':c.score})
    json.dump({'clips':outputs},open(job/'clips.json','w'),indent=2); return job

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('--count',type=int,default=5);p.add_argument('--brief',default='');a=p.parse_args(); print(process(a.url,a.count,a.brief))
