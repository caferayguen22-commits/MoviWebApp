import os
import requests
from flask import Flask, render_template, request, redirect, url_for, abort
from data_manager import DataManager
from models import db, User, Movie

# Base directory for proper database path routing
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configure SQLAlchemy database settings
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect the database instance with the Flask app
db.init_app(app)

# Initialize the DataManager
data_manager = DataManager()

# OMDb API Key (Nutzt einen freien Standardschlüssel für die Abfrage)
OMDB_API_KEY = "tt1285016&apikey=fc258950"


# UPDATED: Home route now renders index.html with all users
@app.route('/')
def index():
    users = data_manager.get_user()
    return render_template('index.html', users=users)


# NEW: Route to handle form submission for creating a user
@app.route('/users', methods=['POST'])
def add_user():
    user_name = request.form.get('name')
    if user_name:
        data_manager.create_user(user_name)
    return redirect(url_for('index'))


# UPDATED: Real route to list all movies of a specific user
@app.route('/users/<int:user_id>')
def list_user_movies(user_id):
    # Fetch user securely using the session helper
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)

    # Use DataManager to get all movies for this user through the Stargate
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', user=user, movies=movies)


# NEW: Route to handle form submission for adding a movie to a user via OMDb API
@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')

    if title:
        # Fetch data dynamically from the OMDb API using the movie title
        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY.split('&apikey=')[1]}"
            response = requests.get(url).json()

            if response.get('Response') == 'True':
                api_title = response.get('Title', title)
                # Extract year safely (handles ranges like '2015–2019')
                raw_year = response.get('Year', '0000')
                api_year = int(raw_year[:4]) if raw_year[:4].isdigit() else 0
                api_director = response.get('Director', 'Unknown Director')
                api_poster = response.get('Poster', '')

                # Create a new Movie object with fetched data
                new_movie = Movie(
                    title=api_title,
                    year=api_year,
                    director=api_director,
                    poster_url=api_poster,
                    user_id=user_id
                )
                data_manager.add_movie(new_movie)
            else:
                print(f"Movie not found on OMDb API: {title}")
        except Exception as e:
            print(f"API or Database Error occurred while adding movie: {e}")
            return "Ups! Da gab es ein Problem bei der Verarbeitung.", 500

    return redirect(url_for('list_user_movies', user_id=user_id))


# NEW: Route to update a movie title using the DataManager
@app.route('/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(movie_id):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        abort(404)

    new_title = request.form.get('title')
    if new_title:
        data_manager.update_movie(movie_id, new_title)

    return redirect(url_for('list_user_movies', user_id=movie.user_id))


# NEW: Route to delete a movie using the DataManager
@app.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        abort(404)

    user_id = movie.user_id
    data_manager.delete_movie(movie_id)

    return redirect(url_for('list_user_movies', user_id=user_id))


# NEW: Custom Error Handler for 404 Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Create database tables and run the application
if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()  # Generates the tables inside movies.db if they don't exist yet
        print("Database initialized successfully! 🦚")
    except Exception as e:
        print(f"CRITICAL ERROR: Could not initialize database: {e}")

    # Adjusted host and port configuration to fully comply with Codio environment access
    app.run(host='0.0.0.0', port=5002, debug=True)