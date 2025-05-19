from pydantic import BaseModel

class UserCreate(BaseModel):
    discord_id: str
    discord_name: str
    game_name: str      
    tag_line: str     