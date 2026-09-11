import threading, uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import process
app=FastAPI(title='ClipForge local worker'); jobs={}
class Request(BaseModel): url:str; brief:str=''; clipCount:int=5; jobId:str|None=None
def run(job_id,r):
    jobs[job_id]={'status':'processing','progress':10,'clips':[]}
    try:
        path=process(r.url,r.clipCount,r.brief); jobs[job_id]={'status':'complete','progress':100,'clips':[], 'jobPath':str(path)}
    except Exception as e: jobs[job_id]={'status':'failed','progress':100,'clips':[],'error':str(e)}
@app.post('/api/process')
def start(r:Request):
    job_id=r.jobId or uuid.uuid4().hex; jobs[job_id]={'status':'queued','progress':0,'clips':[]}; threading.Thread(target=run,args=(job_id,r),daemon=True).start(); return {'jobId':job_id,'status':'queued','progress':0,'clips':[]}
@app.get('/api/process/{job_id}')
def status(job_id:str):
    if job_id not in jobs: raise HTTPException(404,'Job not found')
    return {'jobId':job_id,**jobs[job_id]}
