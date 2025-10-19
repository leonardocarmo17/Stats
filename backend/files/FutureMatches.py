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

        for page in all_data:
            for item in page:
                match_date = datetime.fromisoformat(item["date"].replace("Z", "+00:00"))
                if match_date > now:
                    next_matches.append(item)
        with open(self.next_matches,"w",encoding="utf-8") as f:
            json.dump(next_matches,f,ensure_ascii=False,indent=2)
