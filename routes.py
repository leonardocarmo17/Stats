from flask import Blueprint, render_template, url_for, redirect
from backend.files.TournamentFind import TournamentFind
from backend import MainData

Home = Blueprint("home", __name__)
tournament = TournamentFind()

def RestartData():
    update = MainData.exec()
    return update

@Home.route("/")
def home():
    data_next_matches = tournament.FutureMatchesFinder()
    if not data_next_matches:
        RestartData() 
        data_next_matches = tournament.FutureMatchesFinder() 
    return render_template("home.html", matches=data_next_matches)

@Home.route("/restart", methods=["POST"])
def restart():
    restart_done = RestartData()
    if restart_done:
        return redirect(url_for("home.home"))
    else:
        data_next_matches = tournament.FutureMatchesFinder()
        return render_template("home.html", matches=data_next_matches, message="Nenhuma atualização realizada")
