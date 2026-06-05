from flask import Flask, redirect, render_template, request, url_for

from data_manager import DataManager
from models import Movie, db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moviwebapp.db"

db.init_app(app)
data_manager = DataManager()


@app.route("/")
def index():
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    name = request.form["name"]
    data_manager.create_user(name)
    return redirect(url_for("index"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
