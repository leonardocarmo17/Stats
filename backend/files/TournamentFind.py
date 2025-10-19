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
                "player1": {"name": player1, **default_stats(player1)},
                "player2": {"name": player2, **default_stats(player2)}
            }

        entry = all_stats[key]
        p1_some_data = next(v for v in entry.values() if v["name"].lower() == player1.lower())
        p2_some_data = next(v for v in entry.values() if v["name"].lower() == player2.lower())

        keys = ["win","draw","loss","win_rate","draw_rate"]
        p1_some_data = {k: p1_some_data[k] for k in keys}
        p2_some_data = {k: p2_some_data[k] for k in keys}
        return {
            "player1": p1_some_data,
            "player2": p2_some_data
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