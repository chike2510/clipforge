# ClipForge

ClipForge is a local-first AI video clipping MVP. It accepts YouTube and Twitch URLs, downloads permitted public media with `yt-dlp`, extracts 16 kHz mono audio with FFmpeg, transcribes with `faster-whisper`, ranks candidate moments, refines boundaries, and renders 9:16 MP4 clips with FFmpeg.

## Run the hosted UI

```bash
npm install
npm run dev
```

The Vercel deployment is the creator interface. Because Vercel functions do not ship with FFmpeg, yt-dlp, or a long-running Whisper runtime, hosted processing is intentionally not faked: the UI reports that it needs a worker.

## Run the real local worker

Install FFmpeg, Python 3.11+, then:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn engine.api:app --host 127.0.0.1 --port 8787
LOCAL_ENGINE_URL=http://127.0.0.1:8787 npm run dev
```

For a direct CLI run:

```bash
python engine/main.py 'https://www.youtube.com/watch?v=VIDEO_ID' --count 5
```

Only process videos you own or are permitted to download. Twitch VOD availability depends on the channel and platform permissions. The first Whisper run downloads the `tiny` model locally.

## Architecture

The `app/` layer is a thin Next.js UI/API shell. The `engine/` layer owns source detection, ingestion, transcription, scoring, natural boundary refinement, reframing, and rendering so it can later move to a dedicated worker without rewriting the interface.

## Deployment

Push the repository to GitHub and link the production branch to Vercel. Set `LOCAL_ENGINE_URL` only when the worker is reachable from the deployment; localhost is not reachable from Vercel. For zero-cost local validation, run both the UI and worker on the same machine.
