import httpx
import os
from dotenv import load_dotenv

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
headers = {"X-Riot-Token": RIOT_API_KEY}

async def get_puuid_from_riot_id(game_name: str, tag_line: str) -> str:
    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print(f"[Riot API] PUUID 요청 URL: {url}")
        print(f"[Riot API] 응답 코드: {response.status_code}")
        print(f"[Riot API] 응답 내용: {response.text}")
        if response.status_code == 200:
            return response.json()["puuid"]
        else:
            raise Exception(f"Riot ID → PUUID 실패: {response.status_code} - {response.text}")

async def get_summoner_data_by_puuid(puuid: str) -> dict:
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print(f"[Riot API] 소환사 정보 요청 URL: {url}")
        print(f"[Riot API] 응답 코드: {response.status_code}")
        print(f"[Riot API] 응답 내용: {response.text}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"PUUID → 소환사 정보 실패: {response.status_code} - {response.text}")
