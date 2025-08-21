from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./taoworks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, default="")

class Presentation(Base):
    __tablename__ = "presentations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String, nullable=False)
    topic = Column(String, default="")
    outline = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    pptx_path = Column(String, default="")
    pdf_path = Column(String, default="")
    audio_path = Column(String, default="")

def init_db():
    Base.metadata.create_all(bind=engine)
