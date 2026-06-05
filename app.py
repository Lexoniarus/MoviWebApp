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


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def list_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=movies, user_id=user_id)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    movie = Movie(
        name=request.form["name"],
        director=request.form["director"],
        year=int(request.form["year"]),
        poster_url=request.form["poster_url"],
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


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
