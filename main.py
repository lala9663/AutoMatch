from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas import UserCreate
import crud, models
from utils.riot import get_puuid_from_riot_id, get_summoner_data_by_puuid
from utils.match import start_match_logic
from utils.discord import format_match_result


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

@app.post("/discord-webhook")
async def discord_webhook(req: Request, db = Depends(get_db)):
    body = await req.json()
    # 1) 슬래시 커맨드 타입 및 이름 확인
    if body.get('type') != 2 or body['data']['name'] != 'start-match':
        return {"type": 1}

    # 2) fixed 옵션 파싱
    fixed = ''
    for opt in body['data'].get('options', []):
        if opt['name'] == 'fixed':
            fixed = opt['value']

    # 3) 매칭 로직 실행
    try:
        result = await start_match_logic(fixed, db)
    except Exception as e:
        return {"type": 4, "data": {"content": f"오류 발생: {e}"}}

    # 4) 결과 포맷 및 반환
    content = format_match_result(result)
    return {"type": 4, "data": {"content": content}}