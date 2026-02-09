import json
from operator import itemgetter
from backend.utils.StatsPlayer import DatetimeBrasilia,PlayerFace
import os
from backend.utils.TournamentName import get_tournament_name

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

        try:
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
        except (StopIteration, KeyError) as e:
            print(f"[WARNING] Erro ao buscar stats para {player1} vs {player2}: {e}")
            return {
                "player1": {"name": player1, **default_stats(player1)},
                "player2": {"name": player2, **default_stats(player2)}
            }
    
    def FutureMatchesFinder(self):
        all_data = self.FullData(self.data_futute)
        if all_data:
            tournament_stats = []
            seen_ids = set()  

            for item in all_data:
                try:
                    id = item["id"]
                    
                    if id in seen_ids:
                        print(f"[WARNING] ID duplicado encontrado: {id}. Ignorando segunda ocorrência.")
                        continue
                    seen_ids.add(id)
                    
                    original_date = item["date"]
                    date_obj = DatetimeBrasilia(original_date, return_datetime=True)
                    tournament_name = item["tournament"]["token_international"]
                    tournament_location = item["console"]["id"]
                    tournament_location_name = get_tournament_name(tournament_location)
                    p1_picture_api = item["participant1"]["photo"]
                    p2_picture_api = item["participant2"]["photo"]
                    p1_picture = PlayerFace(p1_picture_api)
                    p2_picture = PlayerFace(p2_picture_api)
                    p1 = item["participant1"]["nickname"]
                    p2 = item["participant2"]["nickname"]
                    
                    try:
                        players = self.Stats(p1, p2)
                        player1 = players["player1"]
                        player2 = players["player2"]
                    except Exception as e:
                        print(f"[WARNING] Erro ao buscar stats para {p1} vs {p2}: {e}. Usando stats padrão.")
                        player1 = {"win": 0, "draw": 0, "loss": 0, "win_rate": 0, "draw_rate": 0}
                        player2 = {"win": 0, "draw": 0, "loss": 0, "win_rate": 0, "draw_rate": 0}

                    match_data = {
                        "id": id,
                        "date": date_obj,  
                        "tournament_name": tournament_name,
                        "tournament_location": tournament_location_name,
                        "console_id": tournament_location,
                        "player1_name": p1,
                        "player2_name": p2,
                        "player1_stats": player1,
                        "player2_stats": player2,
                        "player1_picture": p1_picture,
                        "player2_picture": p2_picture
                    }
                    tournament_stats.append(match_data)
                except Exception as e:
                    print(f"[ERROR] Erro ao processar match ID {item.get('id')}: {type(e).__name__}: {e}")
                    continue
            
            tournament_stats.sort(key=itemgetter("date"))
            
            for t in tournament_stats:
                t["date_str"] = t["date"].strftime("%d/%m/%Y %H:%M")

            from collections import defaultdict
            stadium_time_groups = defaultdict(lambda: defaultdict(list))
            for match in tournament_stats:
                stadium = match["tournament_location"]
                time = match["date_str"]
                stadium_time_groups[stadium][time].append({
                    "id": match["id"],
                    "p1": match["player1_name"],
                    "p2": match["player2_name"]
                })
            
            multi_count = 0
            for stadium in sorted(stadium_time_groups.keys()):
                for time in sorted(stadium_time_groups[stadium].keys()):
                    matches = stadium_time_groups[stadium][time]
                    if len(matches) > 1:
                        multi_count += 1
                        if multi_count <= 5: 
                            print(f"[DEBUG] {stadium} | {time}: {len(matches)} matches")
                            for m in matches:
                                print(f"        ID:{m['id']:8d} | {m['p1']:15s} vs {m['p2']:15s}")
            
            return tournament_stats
        else:
            print("Not found")
            return []