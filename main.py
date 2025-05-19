from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import crud
from schemas import UserCreate

app = FastAPI()

# 테이블 생성
Base.metadata.create_all(bind=engine)

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello AutoMatch!"}

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)
