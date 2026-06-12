from models import db, User, Movie

class DataManager:

    def create_user(self, name):
        """Fügt einen neuen Nutzer zur Datenbank hinzu."""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_user(self):
        """Gibt eine Liste aller registrierten Nutzer zurück"""
        return User.query.all()

    def get_movies(self, user_id):
        """Gibt alle Lieblingsfilme eines bestimmten Nutzers zurück."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """Fügt ein bereits erstelltes Movie_Objekt zur Datenbank hinzu."""
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """Aktualisiert ein Titel eines bestimmten Films anhand seiner ID."""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()

    def delete_movie(self, movie_id):
        """Löscht einen Film komplett aus der Datenbank."""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()