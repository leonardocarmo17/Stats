import json
from datetime import datetime, timezone

class FutureMatches:
    def __init__(self):
        self.data = "backend/json/data.json"
        self.next_matches = "backend/json/next_matches.json"
    def FullData(self):
        with open(self.data,"r",encoding="utf-8") as f:
            data = json.load(f)
        return data
    def NextMatches(self):
        all_data = self.FullData()
        next_matches = []
        now = datetime.now(timezone.utc)
        
        total_matches = 0
        future_count = 0
        past_count = 0

        for page in all_data:
            for item in page:
                total_matches += 1
                match_date = datetime.fromisoformat(item["date"].replace("Z", "+00:00"))
                if match_date > now:
                    future_count += 1
                    next_matches.append(item)
                else:
                    past_count += 1
        
        print(f"[FutureMatches] Total matches no data.json: {total_matches}")
        print(f"[FutureMatches] Matches futuros: {future_count}")
        print(f"[FutureMatches] Matches passados: {past_count}")
        print(f"[FutureMatches] Now (UTC): {now}")
        if total_matches > 0:
            # Mostrar datas do primeiro e último match
            all_dates = []
            for page in all_data:
                for item in page:
                    all_dates.append(item["date"])
            all_dates.sort()
            print(f"[FutureMatches] Primeiro match: {all_dates[0]}")
            print(f"[FutureMatches] Último match: {all_dates[-1]}")
        
        with open(self.next_matches,"w",encoding="utf-8") as f:
            json.dump(next_matches,f,ensure_ascii=False,indent=2)
