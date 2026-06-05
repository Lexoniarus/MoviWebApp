from flask import Flask

from data_manager import DataManager
from models import Movie, db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moviwebapp.db"

db.init_app(app)
data_manager = DataManager()


@app.route("/")
def home():
    return "Welcome to MoviWeb App!"


@app.route("/users")
def list_users():
    users = data_manager.get_users()
    return str(users)


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
