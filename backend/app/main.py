import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    nickname = Column(String, primary_key=True)
    starts = Column(Integer, default=0)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

class StartRequest(BaseModel):
    nickname: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/quiz/start")
def start_quiz(req: StartRequest):

    db = SessionLocal()

    user = db.query(User).filter(User.nickname == req.nickname).first()

    if user is None:
        user = User(nickname=req.nickname, starts=1)
        db.add(user)
    else:
        user.starts += 1

    db.commit()
    db.refresh(user)
    db.close()

    return {
        "nickname": user.nickname,
        "starts": user.starts
    }
    