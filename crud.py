from models import User
from sqlalchemy.orm import Session
from schemas import UserCreate

def create_user(db: Session, user: UserCreate, puuid: str, summoner_name: str):
    db_user = User(
        discord_id=user.discord_id,
        discord_name=user.discord_name,
        summoner_name=summoner_name,
        puuid=puuid
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
