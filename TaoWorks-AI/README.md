# TaoWorks AI

A (reference) open-source tool to **research → generate slides (PPTX/PDF) → add AI voice-over**.
Monorepo includes **FastAPI backend** and **Vite + React frontend**.

> ⚠️ Notes
> - You must set API keys in `.env` (see `.env.example`). OpenAI is used for LLM + TTS by default.
> - For web search / verification, this template integrates a pluggable provider (default: stub).
>   Replace with your preferred service (e.g., Tavily, Serper, Bing, Google CSE).
> - **Canva assets**: this project does _not_ embed proprietary Canva media.
>   Use legally licensed, open assets (Unsplash, Pexels, etc.) or your own Canva exports.

---

## Features
- **Auth**: Email/password (FastAPI + JWT). (Social auth stub on frontend to plug into Firebase/Supabase if desired.)
- **Deep Research**: LLM analysis pipeline + optional web-search provider for fact gathering & citations.
- **Slides**: Auto-generate PPTX with `python-pptx`, plus PDF export.
- **Voice-over**: AI TTS per slide or whole deck (OpenAI TTS out-of-the-box).
- **History**: Save, edit, re-generate, re-download presentations.

---

## Quick Start (Dev)

### 1) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# copy and edit env
cp .env.example .env

# run
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend
```bash
cd frontend
# Node 18+ recommended
npm i
# copy and edit env (optional; only needed if you deploy frontend separately)
cp .env.example .env
npm run dev
```

Open http://localhost:5173 (frontend) and ensure backend is at http://localhost:8000.

---

## Build to a single .exe (optional)

> For a desktop-style bundle that launches the backend and opens the UI.

```bash
# Inside backend venv
pip install pyinstaller
pyinstaller --onefile --name TaoWorksAI server_launcher.py
# Output at: dist/TaoWorksAI (or TaoWorksAI.exe on Windows)
```

Running the executable will start the API server (on 8000 by default). The frontend can be
served separately (build & host) or you can package a static build with a minimal local webview.
See `desktop/README.md` for options.

---

## Deploy

- **Docker**: `docker compose up --build`
- **Render/Fly/Heroku**: Use the included `Procfile` and env vars.
- **Static Frontend**: `npm run build` → deploy `frontend/dist` to static hosting (Netlify/Vercel).
  Point it to your backend URL via `VITE_API_BASE` env.

---

## Legal & Content
- Ensure you have rights to any images, icons, effects you use.
- This template includes open-source code; see `LICENSE` for MIT terms.
- Always review LLM outputs and citations for accuracy before publishing.

---

## Folder Structure
```
TaoWorks-AI/
  backend/
  frontend/
  desktop/
  docker-compose.yml
  LICENSE
  README.md
```

Enjoy & build on it! ⭐
