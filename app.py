from flask import Flask
from routes import Home
def create_app():
    app = Flask(__name__)
    app.register_blueprint(Home) 
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0",port=2000,debug=True)

# No site:
# arrumar o horario (Need QA)