import json
from operator import itemgetter
from backend.utils.StatsPlayer import DatetimeBrasilia,PlayerFace
import os
class TournamentFind:
    def __init__(self):
        self.data_futute = "backend/json/next_matches.json"
        self.stats_original = "backend/json/player_stats.json"

    def FullData(self, file):
        if not os.path.exists(file) or os.path.getsize(file) == 0:
            return []  
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    def Stats(self, player1, player2):
        all_stats = self.FullData(self.stats_original)
        key = "_vs_".join(sorted([player1.lower(), player2.lower()]))

        default_stats = lambda name: {k: 0 for k in ["win","draw","loss","win_rate","draw_rate"]}
        if key not in all_stats:
            return {
                "player1": {"name": player1, **default_stats(player1), "scores": [], "dates": []},
                "player2": {"name": player2, **default_stats(player2), "scores": [], "dates": []}
            }

        entry = all_stats[key]
        
        # Extrai dados de player1 e player2
        p1_data = entry.get("player1", {})
        p2_data = entry.get("player2", {})
        
        keys = ["win","draw","loss","win_rate","draw_rate"]
        p1_stats = {k: p1_data.get(k, 0) for k in keys}
        p2_stats = {k: p2_data.get(k, 0) for k in keys}
        
        # Verifica qual jogador é qual na chave ordenada
        p1_stored_name = entry.get("player1", {}).get("name", "").lower()
        p2_stored_name = entry.get("player2", {}).get("name", "").lower()
        
        # Se os nomes estão invertidos, inverte os scores também
        p1_scores = entry.get("player1_scores", [])
        p2_scores = entry.get("player2_scores", [])
        p1_dates = entry.get("player1_dates", [])
        p2_dates = entry.get("player2_dates", [])
        
        if p1_stored_name == player2.lower() and p2_stored_name == player1.lower():
            p1_scores, p2_scores = p2_scores, p1_scores
            p1_dates, p2_dates = p2_dates, p1_dates
        
        return {
            "player1": {**p1_stats, "scores": p1_scores, "dates": p1_dates},
            "player2": {**p2_stats, "scores": p2_scores, "dates": p2_dates}
        }
    
    def FutureMatchesFinder(self):
        all_data = self.FullData(self.data_futute)
        if all_data:
            tournament_stats = []
            for item in all_data:
                id = item["id"]
                original_date = item["date"]
                date_obj = DatetimeBrasilia(original_date, return_datetime=True)
                tournament_name = item["tournament"]["token_international"]
                p1_picture_api = item["participant1"]["photo"]
                p2_picture_api = item["participant2"]["photo"]
                p1_picture = PlayerFace(p1_picture_api)
                p2_picture = PlayerFace(p2_picture_api)
                p1 = item["participant1"]["nickname"]
                p2 = item["participant2"]["nickname"]
                players = self.Stats(p1, p2)
                player1 = players["player1"]
                player2 = players["player2"]

                tournament_stats.append({
                    "id": id,
                    "date": date_obj,  
                    "tournament_name": tournament_name,
                    "player1_name": p1,
                    "player2_name": p2,
                    "player1_stats": player1,
                    "player2_stats": player2,
                    "player1_picture": p1_picture,
                    "player2_picture": p2_picture
                })
            tournament_stats.sort(key=itemgetter("date"))
            for t in tournament_stats:
                t["date_str"] = t["date"].strftime("%d/%m/%Y %H:%M")

            return tournament_stats
        else:
            print("Not found")