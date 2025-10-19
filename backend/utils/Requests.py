import requests
def request_matches(url):
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if response.status_code < 400:
            return response.json()
        else:
            return None
        
def request_tournament(url):
    response = requests.get(url, timeout=5)
    if response.status_code < 400:
        data = response.json()
        tournaments = data.get("tournaments", [])
        return [f"https://football.esportsbattle.com/api/tournaments/{t['id']}/matches" for t in tournaments if t.get("id")]
    else:
        return None