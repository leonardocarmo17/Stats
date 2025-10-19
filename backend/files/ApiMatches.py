import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from backend.utils.GenerateUrls import generate_urls
from backend.utils.Requests import request_matches, request_tournament
from backend.utils.DeleteData import delete_data

class ApiMatches:
    def __init__(self):
        self.urls_json = []
        self.data_json = []
        self.location = 2
        self.matches_file = "backend/json/matches.json"
        self.data_matches_file = "backend/json/data.json"

    def exec(self):
        delete_data()
        tournament_urls = generate_urls(2)

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(request_tournament, url): url for url in tournament_urls}
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    self.urls_json.extend(result)

        with open(self.matches_file, "w", encoding="utf-8") as f:
            json.dump(self.urls_json, f, indent=2, ensure_ascii=False)

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(request_matches, url): url for url in self.urls_json}
            for future in as_completed(future_to_url):
                data = future.result()
                if data:
                    self.data_json.append(data)

        seen_ids = set()
        cleaned_data = []
        for group in self.data_json: 
            cleaned_group = []
            for match in group:
                match_id = match.get("id")
                if match_id not in seen_ids:
                    seen_ids.add(match_id)
                    cleaned_group.append(match)
                else:
                    # se for duplicado, ignora (remove o primeiro que apareceu)
                    # isso faz com que o segundo permaneça
                    # então precisamos inverter a lógica:
                    # → remove o primeiro e mantém o segundo
                    # solução: reescrever a lógica abaixo
                    pass
            cleaned_data.append(cleaned_group)

        seen_ids.clear()
        final_data = []
        for group in reversed(cleaned_data):
            cleaned_group = []
            for match in group:
                match_id = match.get("id")
                if match_id not in seen_ids:
                    seen_ids.add(match_id)
                    cleaned_group.append(match)

            final_data.append(list(reversed(cleaned_group)))
        final_data = list(reversed(final_data))

        with open(self.data_matches_file, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)

        return True