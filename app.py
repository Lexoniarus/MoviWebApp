import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from flask import Flask, redirect, render_template, request, url_for

from data_manager import DataManager
from models import Movie, db


OMDB_API_URL = "http://www.omdbapi.com/"


def load_env_file():
    env_path = Path(".env")

    if not env_path.exists():
        return

    with env_path.open(encoding="utf-8") as env_file:
        for line in env_file:
            key_value = line.strip()

            if not key_value or key_value.startswith("#"):
                continue

            key, separator, value = key_value.partition("=")

            if separator:
                os.environ.setdefault(key, value.strip("\"'"))


def parse_year(year_text):
    for index in range(len(year_text) - 3):
        year = year_text[index:index + 4]

        if year.isdigit():
            return int(year)

    return 0


def fetch_movie_data(title):
    api_key = os.environ.get("OMDB_API_KEY")

    if not api_key:
        return None

    query = urlencode({"t": title, "apikey": api_key})

    with urlopen(f"{OMDB_API_URL}?{query}", timeout=10) as response:
        movie_data = json.loads(response.read().decode("utf-8"))

    if movie_data.get("Response") == "False":
        return None

    return {
        "name": movie_data.get("Title", title),
        "director": movie_data.get("Director", "Unknown"),
        "year": parse_year(movie_data.get("Year", "")),
        "poster_url": movie_data.get("Poster", ""),
    }


load_env_file()

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


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def list_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=movies, user_id=user_id)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    movie_data = fetch_movie_data(request.form["name"])

    if movie_data is None:
        return redirect(url_for("list_movies", user_id=user_id))

    movie = Movie(
        name=movie_data["name"],
        director=movie_data["director"],
        year=movie_data["year"],
        poster_url=movie_data["poster_url"],
        user_id=user_id,
    )
    data_manager.add_movie(movie)
    return redirect(url_for("list_movies", user_id=user_id))


@app.route(
    "/users/<int:user_id>/movies/<int:movie_id>/update",
    methods=["POST"],
)
def update_movie(user_id, movie_id):
    new_title = request.form["new_title"]
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for("list_movies", user_id=user_id))


@app.route(
    "/users/<int:user_id>/movies/<int:movie_id>/delete",
    methods=["POST"],
)
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for("list_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
