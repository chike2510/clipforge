import { NextResponse } from 'next/server';
export async function GET(_req: Request, {params}:{params:{jobId:string}}){
  const localEngine=process.env.LOCAL_ENGINE_URL;
  if(localEngine){try{const r=await fetch(`${localEngine}/api/process/${params.jobId}`,{cache:'no-store'});return NextResponse.json(await r.json(),{status:r.status})}catch{}}
  return NextResponse.json({jobId:params.jobId,status:'queued',progress:0,clips:[],deploymentNotice:'Waiting for a local worker. Run the Python engine from the repository and set LOCAL_ENGINE_URL.'});
}
