import sys, os
import asyncio

# 1) 프로젝트 루트를 import 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.lcu import get_lcu_participants

async def main():
    # 2) LCU 참가자 가져오기
    participants = await get_lcu_participants()
    print("Lobby participants:", participants)

if __name__ == "__main__":
    asyncio.run(main())
