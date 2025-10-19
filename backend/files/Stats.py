import json
import os
from backend.utils.MatchResults import compute_stats_for_pair
class Stats:
    def __init__(self):
        self.data_file = "backend/json/data.json"
        self.next_file = "backend/json/next_matches.json"
        self.output_path = "backend/json/player_stats.json"

    def load_json(self, file_path):
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self.flatten(data)

    def flatten(self, data):
        flat = []
        for item in data:
            if isinstance(item, list):
                flat.extend(item)
            elif isinstance(item, dict):
                flat.append(item)
        return flat
    def calculate_stats(self):
        historical = self.load_json(self.data_file)
        next_matches = self.load_json(self.next_file)

        results = {}
        processed_keys = set()

        for match in next_matches:
            try:
                p1 = match["participant1"]["nickname"]
                p2 = match["participant2"]["nickname"]
            except KeyError:
                continue

            key = "_vs_".join(sorted([p1.lower(), p2.lower()]))
            if key in processed_keys:
                continue
            processed_keys.add(key)

            stats, total_matches = compute_stats_for_pair(p1, p2, historical)
            results[key] = {
                "player1": {"name": p1, **stats[p1]},
                "player2": {"name": p2, **stats[p2]},
                "total_matches": total_matches
            }
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        return results
