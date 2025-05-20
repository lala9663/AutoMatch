import os, base64, httpx
from typing import List

# League Client Lockfile 경로 (Windows 예시)
LOCKFILE_PATH = r"C:\Riot Games\League of Legends\lockfile"

async def get_lcu_participants() -> List[str]:
    """
    커스텀 로비 또는 챔피언 선택 단계에서
    참가자들의 소환사명을 리스트로 반환합니다.
    """
    # 1) Lockfile 읽기
    with open(LOCKFILE_PATH, 'r') as f:
        parts = f.read().split(':')
        port     = parts[2]
        password = parts[3]
        protocol = parts[4]

    # 2) Basic Auth 헤더 생성
    token = base64.b64encode(f"riot:{password}".encode()).decode()
    headers = {
        'Authorization': f'Basic {token}',
        'Accept': 'application/json'
    }

    # 3) 로비 단계 참가자 조회
    url_lobby = f"{protocol}://127.0.0.1:{port}/lol-lobby/v2/lobby"
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(url_lobby, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    # gameConfig.customTeam100, customTeam200에서 summonerName 추출
    teams = data.get('gameConfig', {}).get('customTeam100', []) + \
            data.get('gameConfig', {}).get('customTeam200', [])
    participants = [m['summonerName'] for m in teams if m.get('summonerName')]
    if participants:
        return participants

    # 4) 챔피언 선택 단계 참가자 조회 (fallback)
    url_session = f"{protocol}://127.0.0.1:{port}/lol-champ-select/v1/session"
    async with httpx.AsyncClient(verify=False) as client:
        try:
            resp = await client.get(url_session, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError:
            return []
    members = data.get('myTeam', []) + data.get('theirTeam', [])
    return [m['summonerName'] for m in members if m.get('summonerName')]