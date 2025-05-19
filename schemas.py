from pydantic import BaseModel

class UserCreate(BaseModel):
    discord_id: str
    discord_name: str
    summoner_name: str
