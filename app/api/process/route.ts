import { NextResponse } from 'next/server';
export const runtime = 'nodejs';
export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}));
  if (!body.url && !body.fileName) return NextResponse.json({ error: 'Add a YouTube/Twitch URL or upload a video.' }, { status: 400 });
  const id = crypto.randomUUID();
  const localEngine = process.env.LOCAL_ENGINE_URL;
  if (localEngine) {
    try { const r = await fetch(`${localEngine}/api/process`, { method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify({...body, jobId:id}) }); return NextResponse.json(await r.json(), {status:r.status}); } catch {}
  }
  return NextResponse.json({ jobId:id, status:'queued', progress:0, deploymentNotice:'The hosted shell is ready. Connect LOCAL_ENGINE_URL to your local FFmpeg/Whisper worker to process media; Vercel functions do not provide the native video toolchain.' });
}
