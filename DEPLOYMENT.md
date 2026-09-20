# Deployment

The ClipForge web interface is the AutoClip Vite frontend in `frontend/`.

Vercel project settings:

- Root Directory: `frontend`
- Framework Preset: Vite
- Install Command: `npm ci`
- Build Command: `npm run build`
- Output Directory: `dist`

The processing backend is intentionally not deployed as Vercel functions. Run it with Docker or the local startup scripts described in `STARTUP_GUIDE.md`; it requires FFmpeg, Whisper, Redis, and the configured AI provider.
