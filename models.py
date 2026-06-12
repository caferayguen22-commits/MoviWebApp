from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy-Instanz erstellen
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullbase=False)

    # Hilfsmethode für eine saubere Textdarstellung im Terminal
    def __repr__(self):
        return f"<User {self.name}>"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullbase=False)
    director = db.Column(db.String(200), nullbase=False)
    year = db.Column(db.Integer, nullbase=False)
    poster_url = db.Column(db.String(500), nullbase=True)

    # Fremdschlüssel: Verknüpft jeden Film fest mit der ID eines Nutzers
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"