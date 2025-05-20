import random
from typing import List, Dict
from schemas import UserCreate
import crud
from sqlalchemy.orm import Session
from models import User
from utils.lcu import get_lcu_participants

async def start_match_logic(fixed: str, db: Session) -> Dict[str, List[User]]:
    # 1) 고정 페어 파싱 (소환사명 리스트)
    fixed_pair = [name.strip() for name in fixed.split(',') if name.strip()]

    # 2) LCU에서 소환사명 리스트 조회
    summoner_names = await get_lcu_participants()

    # 3) DB에 참가자 등록 또는 조회
    users = []
    for name in summoner_names:
        # tag_line 은 LCU엔 없으므로 빈 문자열
        uc = UserCreate(
            discord_id=name,
            discord_name=name,
            game_name=name,
            tag_line=""
        )
        user = crud.create_or_update_user(db, uc, puuid=None, summoner_name=name)
        users.append(user)

    # 4) 팀 구성 (고정 페어 + 랜덤)
    blue, red = [], []
    for u in users:
        if u.summoner_name in fixed_pair:
            blue.append(u)
    pool = [u for u in users if u.summoner_name not in fixed_pair]
    random.shuffle(pool)
    while pool:
        if len(blue) < 5:
            blue.append(pool.pop())
        else:
            red.append(pool.pop())

    # 5) 랜덤 챔피언 3개 추천
    def pick_champs(u: User):
        champs = getattr(u, 'available_champions', [])
        return random.sample(champs, min(len(champs), 3))

    for team in (blue, red):
        for u in team:
            u.champions = pick_champs(u)

    return {'blue': blue, 'red': red}