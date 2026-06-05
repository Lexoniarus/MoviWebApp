from models import Movie, User, db


class DataManager:
    """Provides CRUD operations for users and movies."""

    def create_user(self, name):
        """Create a new user in the database."""
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user

    def get_users(self):
        """Return all users from the database."""
        return User.query.all()

    def get_movies(self, user_id):
        """Return all movies for a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """Add a movie to the database."""
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, new_title):
        """Update the title of a movie."""
        movie = db.session.get(Movie, movie_id)

        if movie is None:
            return None

        movie.name = new_title
        db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        """Delete a movie from the database."""
        movie = db.session.get(Movie, movie_id)

        if movie is None:
            return None

        db.session.delete(movie)
        db.session.commit()
        return movie
