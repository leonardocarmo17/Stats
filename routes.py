from flask import Blueprint, render_template, url_for, redirect, jsonify
from backend.files.TournamentFind import TournamentFind
from backend.utils.GetTournaments import GetTournaments
from backend.utils.MatchHistory import MatchHistory
from backend import MainData

Home = Blueprint("home", __name__)
tournament = TournamentFind()
get_tournaments = GetTournaments()
match_history = MatchHistory()

def RestartData():
    update = MainData.exec()
    return update

@Home.route("/")
def home():
    data_next_matches = tournament.FutureMatchesFinder()
    stadiums = get_tournaments.get_unique_stadiums()
    print(f"[ROUTE] Enviando {len(data_next_matches)} matches para o template")
    if not data_next_matches:
        RestartData() 
        data_next_matches = tournament.FutureMatchesFinder()
        stadiums = get_tournaments.get_unique_stadiums()
        print(f"[ROUTE] Após restart: {len(data_next_matches)} matches")
    return render_template("home.html", matches=data_next_matches, stadiums=stadiums)

@Home.route("/restart", methods=["POST", "GET"])
def restart():
    print("\n[RESTART] Iniciando recarga de dados da API...")
    restart_done = RestartData()
    print(f"[RESTART] Recarga concluída com sucesso: {restart_done}")
    # Reinicializar tournament object com novos dados
    global tournament
    tournament = TournamentFind()
    if restart_done:
        return redirect(url_for("home.home"))
    else:
        data_next_matches = tournament.FutureMatchesFinder()
        return render_template("home.html", matches=data_next_matches, message="Nenhuma atualização realizada")

@Home.route("/api/head-to-head/<player1>/<player2>", methods=["GET"])
def get_head_to_head(player1, player2):
    """Retorna o histórico de partidas passadas entre dois jogadores"""
    try:
        print(f"\n[H2H API] Requisição recebida: {player1} vs {player2}")
        
        matches, stats = match_history.get_head_to_head(player1, player2)
        
        # Estruturar resposta
        response = {
            "success": True,
            "player1": stats["player1"],
            "player2": stats["player2"],
            "total_matches": stats["total_matches"],
            "matches": []
        }
        
        # Formart matches
        for match in matches:
            try:
                p1 = match["participant1"]
                p2 = match["participant2"]
                
                match_data = {
                    "id": match.get("id"),
                    "date": match.get("date"),
                    "tournament": match.get("tournament_name"),
                    "location": match.get("tournament_location"),
                    "player1": {
                        "name": p1.get("nickname"),
                        "score": p1.get("score"),
                        "picture": p1.get("picture")
                    },
                    "player2": {
                        "name": p2.get("nickname"),
                        "score": p2.get("score"),
                        "picture": p2.get("picture")
                    }
                }
                response["matches"].append(match_data)
            except (KeyError, TypeError):
                continue
        
        print(f"[H2H API] Resposta preparada: {len(response['matches'])} partidas")
        print(f"[H2H API] {player1}: {stats['player1']['wins']}W {stats['player1']['draws']}D {stats['player1']['losses']}L")
        print(f"[H2H API] {player2}: {stats['player2']['wins']}W {stats['player2']['draws']}D {stats['player2']['losses']}L")
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"[H2H API ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "total_matches": 0,
            "matches": []
        }), 500

