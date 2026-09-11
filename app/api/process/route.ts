import { NextResponse } from 'next/server';
export const runtime = 'nodejs';
export const maxDuration = 60;
export async function POST(req: Request) {
  const contentType = req.headers.get('content-type') || '';
  let body: Record<string, unknown> = {};
  let file: File | null = null;
  if (contentType.includes('multipart/form-data')) {
    const form = await req.formData();
    file = form.get('file') instanceof File ? form.get('file') as File : null;
    body = { brief: form.get('brief') || '', clipCount: Number(form.get('clipCount') || 5), fileName: file?.name || '' };
  } else body = await req.json().catch(() => ({}));
  if (!body.url && !file) return NextResponse.json({ error: 'Add a YouTube/Twitch URL or choose a video file.' }, { status: 400 });
  const id = crypto.randomUUID();
  const localEngine = process.env.LOCAL_ENGINE_URL;
  if (localEngine) {
    try {
      if (file) {
        const form = new FormData(); form.append('file', file); form.append('brief', String(body.brief || '')); form.append('clipCount', String(body.clipCount || 5)); form.append('jobId', id);
        const r = await fetch(`${localEngine}/api/process`, { method:'POST', body:form }); return NextResponse.json(await r.json(), {status:r.status});
      }
      const r = await fetch(`${localEngine}/api/process`, { method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify({...body, jobId:id}) }); return NextResponse.json(await r.json(), {status:r.status});
    } catch {}
  }
  return NextResponse.json({ jobId:id, status:'queued', progress:0, deploymentNotice:'The hosted shell is ready. Connect LOCAL_ENGINE_URL to your local FFmpeg/Whisper worker to process media; Vercel functions do not provide the native video toolchain.' });
}
