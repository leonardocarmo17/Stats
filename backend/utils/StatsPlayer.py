from datetime import datetime, timezone, timedelta

def DatetimeBrasilia(iso_date, return_datetime=False):
    utc_time = datetime.fromisoformat(iso_date.replace("Z","+00:00"))
    br_time = utc_time.astimezone(timezone(timedelta(hours=-3)))
    if return_datetime:
        return br_time
    return br_time.strftime("%d/%m/%Y %H:%M")

def PlayerFace(image):
    if image:
        return f"https://football.esportsbattle.com/api/Image/efootball/80x80/{image}"
    else:
        return f"https://cdn-icons-png.flaticon.com/512/2815/2815428.png"
