from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas import UserCreate
import crud, models
from utils.riot import get_puuid_from_riot_id, get_summoner_data_by_puuid
import sys
sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        puuid = await get_puuid_from_riot_id(user.game_name, user.tag_line)
        summoner_info = await get_summoner_data_by_puuid(puuid)
        summoner_name = f"{user.game_name}#{user.tag_line}"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return crud.create_user(db, user, puuid, summoner_name)
