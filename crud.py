from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        discord_id=user.discord_id,
        discord_name=user.discord_name,
        summoner_name=user.summoner_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
