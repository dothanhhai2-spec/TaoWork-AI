from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..services.db import SessionLocal, Presentation, init_db
import os, json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

init_db()
STORAGE = os.getenv("STORAGE_DIR", "./storage")

@router.get("")
def list_presentations(user_id: int):
    db = next(get_db())
    items = db.query(Presentation).filter(Presentation.user_id == user_id).order_by(Presentation.id.desc()).all()
    return [{
        "id": it.id,
        "title": it.title,
        "topic": it.topic,
        "created_at": it.created_at,
        "pptx_path": it.pptx_path,
        "pdf_path": it.pdf_path,
        "audio_path": it.audio_path
    } for it in items]

@router.delete("/{pid}")
def delete_presentation(pid: int, user_id: int):
    db = next(get_db())
    pres = db.query(Presentation).filter(Presentation.id == pid, Presentation.user_id == user_id).first()
    if not pres:
        raise HTTPException(status_code=404, detail="Not found")
    for p in [pres.pptx_path, pres.pdf_path, pres.audio_path]:
        if p and os.path.exists(p): os.remove(p)
    db.delete(pres)
    db.commit()
    return {"ok": True}
