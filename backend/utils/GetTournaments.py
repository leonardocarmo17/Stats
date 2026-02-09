import json
import os
from backend.utils.TournamentName import get_tournament_name


class GetTournaments:
    def __init__(self):
        self.next_matches = "backend/json/next_matches.json"

    def get_unique_stadiums(self):
        """Retorna uma lista de estádios únicos das próximas partidas"""
        if not os.path.exists(self.next_matches) or os.path.getsize(self.next_matches) == 0:
            return []
        
        stadiums = set()
        
        with open(self.next_matches, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for item in data:
            tournament_location = item["console"]["id"]
            stadium_name = get_tournament_name(tournament_location)
            stadiums.add(stadium_name)
        
        # Retorna uma lista ordenada, excluindo "Unknown Tournament"
        stadiums_list = sorted([s for s in stadiums if s != "Unknown Tournament"])
        return stadiums_list
