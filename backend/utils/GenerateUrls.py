from datetime import datetime, timedelta

def generate_urls(location):
    urls = []
    today = datetime.now()
    
    for i in range(-1, 10):
        day = today - timedelta(days=i)
        day_from = day.strftime("%d") 
        month_from = day.strftime("%m") 
        year_from = day.strftime("%Y")
        
        day_to_dt = day + timedelta(days=1)
        day_to = day_to_dt.strftime("%d")
        month_to = day_to_dt.strftime("%m")
        year_to = day_to_dt.strftime("%Y")
        
        url = (
            f"https://football.esportsbattle.com/api/tournaments?"
            f"page=1&dateFrom={year_from}%2F{month_from}%2F{day_from}+03%3A00&"
            f"dateTo={year_to}%2F{month_to}%2F{day_to}+02%3A59&location={location}"
        )
        urls.append(url)
        
    return urls
