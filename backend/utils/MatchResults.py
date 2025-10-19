def get_match_result(s1, s2):
    if s1 is None or s2 is None:
        return None
    if s1 > s2:
        return "win"
    elif s1 < s2:
        return "loss"
    else:
        return "draw"
def compute_stats_for_pair(p1, p2, historical):
    stats = {
        p1: {"win": 0, "draw": 0, "loss": 0},
        p2: {"win": 0, "draw": 0, "loss": 0}
    }
    total_matches = 0

    for past in historical:
        try:
            hp1 = past["participant1"]["nickname"]
            hp2 = past["participant2"]["nickname"]
            s1 = past["participant1"].get("score")
            s2 = past["participant2"].get("score")
        except KeyError:
            continue
        if {hp1.lower(), hp2.lower()} == {p1.lower(), p2.lower()}:
            result = get_match_result(s1, s2)
            if result:
                total_matches += 1
                if hp1.lower() == p1.lower():
                    stats[p1][result] += 1
                    stats[p2][{"win": "loss", "loss": "win", "draw": "draw"}[result]] += 1
                else:
                    stats[p2][result] += 1
                    stats[p1][{"win": "loss", "loss": "win", "draw": "draw"}[result]] += 1

        # Calcula taxas
    for player in (p1, p2):
        for outcome in ["win", "draw", "loss"]:
            stats[player][f"{outcome}_rate"] = round(
                (stats[player][outcome] / total_matches * 100) if total_matches else 0, 1)

    return stats, total_matches