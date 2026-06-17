from models import db, User, Movie

class DataManager:

    def create_user(self, name):
        """Fügt einen neuen Nutzer zur Datenbank hinzu."""
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def get_user(self):
        """Gibt eine Liste aller registrierten Nutzer zurück"""
        return db.session.query(User).all()

    def get_movies(self, user_id):
        """Gibt alle Lieblingsfilme eines bestimmten Nutzers zurück."""
        return db.session.query(Movie).filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """Fügt ein bereits erstelltes Movie_Objekt zur Datenbank hinzu."""
        try:
            db.session.add(movie)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def update_movie(self, movie_id, new_title):
        """Aktualisiert ein Titel eines bestimmten Films anhand seiner ID."""
        try:
            movie = db.session.get(Movie, movie_id)
            if movie:
                movie.title = new_title
                db.session.commit()
                return True
            return False
        except Exception:
            db.session.rollback()
            return False

    def delete_movie(self, movie_id):
        """Löscht einen Film komplett aus der Datenbank."""
        try:
            movie = db.session.get(Movie, movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
                return True
            return False
        except Exception:
            db.session.rollback()
            return False