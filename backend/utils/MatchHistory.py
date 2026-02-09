
import json
import os
from typing import List, Dict, Any, Tuple


class MatchHistory:
    def __init__(self):
        self.data_file = "backend/json/data.json"
    
    def load_all_matches(self) -> List[Dict[str, Any]]:
        """Carrega todos os matches históricos"""
        if not os.path.exists(self.data_file):
            return []
        
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            flat = []
            for item in data:
                if isinstance(item, list):
                    flat.extend(item)
                elif isinstance(item, dict):
                    flat.append(item)
            return flat
        except Exception as e:
            print(f"[ERROR] Ao carregar dados: {e}")
            return []
    
    def get_head_to_head(self, player1: str, player2: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Recupera apenas as partidas passadas entre dois jogadores.
        
        Args:
            player1: Nome do primeiro jogador
            player2: Nome do segundo jogador
            
        Returns:
            Tuple contendo:
            - Lista de partidas passadas ordenadas por data (mais recentes primeiro)
            - Dicionário com estatísticas resumidas
        """
        all_matches = self.load_all_matches()
        
        p1_lower = player1.lower()
        p2_lower = player2.lower()
        
        head_to_head = []
        for match in all_matches:
            try:
                participant1 = match["participant1"]["nickname"].lower()
                participant2 = match["participant2"]["nickname"].lower()
                
                if {participant1, participant2} == {p1_lower, p2_lower}:
                    score1 = match.get("participant1", {}).get("score")
                    score2 = match.get("participant2", {}).get("score")
                    
                    if score1 is not None and score2 is not None:
                        head_to_head.append(match)
            except (KeyError, TypeError):
                continue
        
        head_to_head.sort(
            key=lambda x: x.get("date", ""),
            reverse=True
        )
        
        stats = self._calculate_h2h_stats(player1, player2, head_to_head)
        
        return head_to_head, stats
    
    def _calculate_h2h_stats(self, player1: str, player2: str, matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula estatísticas do confronto direto"""
        stats = {
            "player1": {
                "name": player1,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0
            },
            "player2": {
                "name": player2,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0
            },
            "total_matches": len(matches)
        }
        
        p1_lower = player1.lower()
        p2_lower = player2.lower()
        
        print(f"\n[H2H STATS] Calculando estatísticas para {player1} vs {player2}")
        print(f"[H2H STATS] Total de partidas a processar: {len(matches)}")
        
        for idx, match in enumerate(matches):
            try:
                p1 = match["participant1"]
                p2 = match["participant2"]
                
                p1_score = p1.get("score")
                p2_score = p2.get("score")
                
                if p1["nickname"].lower() == p1_lower:
                    stats["player1"]["goals_for"] += p1_score or 0
                    stats["player1"]["goals_against"] += p2_score or 0
                    stats["player2"]["goals_for"] += p2_score or 0
                    stats["player2"]["goals_against"] += p1_score or 0
                    
                    if p1_score > p2_score:
                        stats["player1"]["wins"] += 1
                        stats["player2"]["losses"] += 1
                    elif p1_score < p2_score:
                        stats["player1"]["losses"] += 1
                        stats["player2"]["wins"] += 1
                    else:
                        stats["player1"]["draws"] += 1
                        stats["player2"]["draws"] += 1
                    
                    print(f"[H2H STATS] Match {idx + 1}: {p1['nickname']} ({p1_score}) vs {p2['nickname']} ({p2_score}) - Player1={p1_lower}")
                else:
                    stats["player1"]["goals_for"] += p2_score or 0
                    stats["player1"]["goals_against"] += p1_score or 0
                    stats["player2"]["goals_for"] += p1_score or 0
                    stats["player2"]["goals_against"] += p2_score or 0
                    
                    if p2_score > p1_score:
                        stats["player1"]["wins"] += 1
                        stats["player2"]["losses"] += 1
                    elif p2_score < p1_score:
                        stats["player1"]["losses"] += 1
                        stats["player2"]["wins"] += 1
                    else:
                        stats["player1"]["draws"] += 1
                        stats["player2"]["draws"] += 1
                    
                    print(f"[H2H STATS] Match {idx + 1}: {p2['nickname']} ({p2_score}) vs {p1['nickname']} ({p1_score}) - Player2={p1_lower}")
            except (KeyError, TypeError) as e:
                print(f"[H2H STATS ERROR] Erro ao processar match {idx + 1}: {e}")
                continue
        
        if stats["total_matches"] > 0:
            stats["player1"]["win_rate"] = round(
                (stats["player1"]["wins"] / stats["total_matches"]) * 100, 1
            )
            stats["player2"]["win_rate"] = round(
                (stats["player2"]["wins"] / stats["total_matches"]) * 100, 1
            )
        else:
            stats["player1"]["win_rate"] = 0
            stats["player2"]["win_rate"] = 0
        
        print(f"[H2H STATS] Resultado final:")
        print(f"  {player1}: {stats['player1']['wins']}W {stats['player1']['draws']}D {stats['player1']['losses']}L")
        print(f"  {player2}: {stats['player2']['wins']}W {stats['player2']['draws']}D {stats['player2']['losses']}L")
        print(f"[H2H STATS] Fin\n")
        
        return stats
