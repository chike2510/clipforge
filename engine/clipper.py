import subprocess
from pathlib import Path

def render_clip(source: str, output: str, start: float, end: float, subtitle: str=''):
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    duration=max(1,end-start)
    vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"
    subprocess.run(['ffmpeg','-y','-ss',str(start),'-i',source,'-t',str(duration),'-vf',vf,'-c:v','libx264','-preset','veryfast','-c:a','aac','-movflags','+faststart',output],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    return output
