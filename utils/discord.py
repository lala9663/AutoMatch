from typing import Dict, List

def format_match_result(result: Dict[str, List]) -> str:
    lines = ['🎮 팀 매칭 결과']
    for side in ('blue', 'red'):
        header = '🔵 Blue 팀' if side == 'blue' else '🔴 Red 팀'
        lines.append(header)
        for u in result[side]:
            champs = ', '.join(u.champions)
            lines.append(f"• {u.summoner_name}: [{champs}]")
        lines.append('')
    return '\n'.join(lines)