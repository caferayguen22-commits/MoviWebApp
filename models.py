from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy-Instanz erstellen
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    # Beziehung zu den Filmen herstellen
    movies = db.relationship('Movie', backref='user', lazy=True)

    # Hilfsmethode für eine saubere Textdarstellung im Terminal
    def __repr__(self):
        return f"<User {self.name}>"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(500), nullable=True)

    # Fremdschlüssel: Verknüpft jeden Film fest mit der ID eines Nutzers
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"