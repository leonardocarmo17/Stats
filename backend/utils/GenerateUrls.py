from datetime import datetime, timedelta
import requests

def generate_urls():
    urls = []
    today = datetime.now()

    locations = ["76", "2", "1", "77", "74", "75", "78", "79", "80", "81", "82", "83", "84", "85"]
    location_params = "&".join([f"location={loc}" for loc in locations])
    
    day_from = today - timedelta(days=4, hours=3)
    day_from_str = day_from.strftime("%d") 
    month_from_str = day_from.strftime("%m") 
    year_from_str = day_from.strftime("%Y")
    hour_from = day_from.strftime("%H")
    min_from = day_from.strftime("%M")
    
    day_to = today + timedelta(days=1, hours=3)
    day_to_str = day_to.strftime("%d")
    month_to_str = day_to.strftime("%m")
    year_to_str = day_to.strftime("%Y")
    hour_to = day_to.strftime("%H")
    min_to = day_to.strftime("%M")
    
    base_url = (
        f"https://football.esportsbattle.com/api/tournaments?"
        f"dateFrom={year_from_str}%2F{month_from_str}%2F{day_from_str}+{hour_from}%3A{min_from}&"
        f"dateTo={year_to_str}%2F{month_to_str}%2F{day_to_str}+{hour_to}%3A{min_to}&{location_params}"
    )
    
    first_url = f"{base_url}&page=1"
    try:
        response = requests.get(first_url, timeout=5)
        if response.status_code < 400:
            data = response.json()
            total_pages = data.get("totalPages", 1)
            print(f"[GenerateUrls] Total de páginas na API: {total_pages}")
        else:
            total_pages = 5
            print(f"[GenerateUrls] Erro ao buscar totalPages, usando padrão: {total_pages}")
    except Exception as e:
        total_pages = 5
        print(f"[GenerateUrls] Exceção ao buscar totalPages: {e}, usando padrão: {total_pages}")
    
    for page in range(1, total_pages + 1):
        url = f"{base_url}&page={page}"
        urls.append(url)
        print(f"[GenerateUrls] URL Page {page}/{total_pages}: {url[:100]}...")
        
    return urls
        
    return urls
