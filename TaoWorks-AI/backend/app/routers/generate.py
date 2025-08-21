from fastapi import APIRouter, Form
from sqlalchemy.orm import Session
from ..services.db import SessionLocal, Presentation, init_db
from ..services.llm import draft_outline
from ..services.slides import make_pptx, make_pdf_from_outline
from ..services.tts import synthesize_voice
import os, json, tempfile

router = APIRouter()
init_db()
STORAGE = os.getenv("STORAGE_DIR", "./storage")

@router.post("")
def generate(user_id: int = Form(...), title: str = Form(...), topic: str = Form(""), raw_text: str = Form("")):
    os.makedirs(STORAGE, exist_ok=True)
    outline = draft_outline(topic or title, raw_text)
    # Save files
    pptx_path = os.path.join(STORAGE, f"pres_{user_id}_{title.replace(' ','_')}.pptx")
    pdf_path = os.path.join(STORAGE, f"pres_{user_id}_{title.replace(' ','_')}.pdf")
    audio_path = os.path.join(STORAGE, f"pres_{user_id}_{title.replace(' ','_')}.mp3")

    make_pptx(outline, pptx_path, title=title)
    # Concatenate notes for voice-over
    notes_text = "\n".join([s.get("notes","") or s.get("title","") for s in outline])
    if notes_text.strip():
        synthesize_voice(notes_text, audio_path)
    else:
        audio_path = ""

    make_pdf_from_outline(outline, pdf_path, title)

    # Persist
    db = SessionLocal()
    pres = Presentation(user_id=user_id, title=title, topic=topic, outline=json.dumps(outline),
                        pptx_path=pptx_path, pdf_path=pdf_path, audio_path=audio_path)
    db.add(pres)
    db.commit()
    db.refresh(pres)
    return {"id": pres.id, "title": pres.title, "pptx_path": pres.pptx_path, "pdf_path": pres.pdf_path, "audio_path": pres.audio_path}
