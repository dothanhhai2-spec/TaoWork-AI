from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..services.db import SessionLocal, init_db, User
from ..services.auth import get_password_hash, verify_password, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

init_db()

@router.post("/register")
def register(email: str, password: str, name: str = ""):
    db = next(get_db())
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=email, password_hash=get_password_hash(password), name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email, "name": user.name}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = next(get_db())
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "name": user.name}}
