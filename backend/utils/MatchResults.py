def get_match_result(s1, s2):
    if s1 is None or s2 is None:
        return None
    if s1 > s2:
        return "win"
    elif s1 < s2:
        return "loss"
    else:
        return "draw"

def format_date(date_str):
    if not date_str:
        return ""
    try:
        from backend.utils.StatsPlayer import DatetimeBrasilia
        return DatetimeBrasilia(date_str, return_datetime=False)
    except:
        return date_str
def compute_stats_for_pair(p1, p2, historical):
    stats = {
        p1: {"win": 0, "draw": 0, "loss": 0},
        p2: {"win": 0, "draw": 0, "loss": 0}
    }
    total_matches = 0
    scores = {
        p1: [],
        p2: []
    }
    dates = {
        p1: [],
        p2: []
    }

    for past in historical:
        try:
            hp1 = past["participant1"]["nickname"]
            hp2 = past["participant2"]["nickname"]
            s1 = past["participant1"].get("score")
            s2 = past["participant2"].get("score")
            match_date = past.get("date", "")
            
        except KeyError:
            continue
        if {hp1.lower(), hp2.lower()} == {p1.lower(), p2.lower()}:
            result = get_match_result(s1, s2)
            if result:
                total_matches += 1
                formatted_date = format_date(match_date)
                if hp1.lower() == p1.lower():
                    stats[p1][result] += 1
                    stats[p2][{"win": "loss", "loss": "win", "draw": "draw"}[result]] += 1
                    scores[p1].append(s1)
                    scores[p2].append(s2)
                    dates[p1].append(formatted_date)
                    dates[p2].append(formatted_date)
                else:
                    stats[p2][result] += 1
                    stats[p1][{"win": "loss", "loss": "win", "draw": "draw"}[result]] += 1
                    scores[p2].append(s1)
                    scores[p1].append(s2)
                    dates[p2].append(formatted_date)
                    dates[p1].append(formatted_date)

        # Calcula taxas
    for player in (p1, p2):
        for outcome in ["win", "draw", "loss"]:
            stats[player][f"{outcome}_rate"] = round(
                (stats[player][outcome] / total_matches * 100) if total_matches else 0, 1)

    return stats, total_matches, scores, dates