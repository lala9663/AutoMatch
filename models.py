from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = "users"

    discord_id = Column(String, primary_key=True, index=True)
    discord_name = Column(String)
    summoner_name = Column(String)
    puuid = Column(String, unique=True, index=True) # 나중에 Riot API로 채움
