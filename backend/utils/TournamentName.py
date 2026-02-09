def get_tournament_name(tournament_token):
    if tournament_token == 139 or tournament_token == 140:
        return "Hillsborough"
    elif tournament_token == 136 or tournament_token == 137:
        return "Anfield"
    elif tournament_token == 154 or tournament_token == 155:
        return "Stamford Bridge"
    elif tournament_token == 3 or tournament_token == 4:
        return "Wembley"
    elif tournament_token == 1 or tournament_token == 2:
        return "Old Trafford"
    else:
        return "Unknown Tournament"