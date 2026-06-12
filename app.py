import os
from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db

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
    # We simply use the exact same logic as in our DataManager to get the user by ID
    from models import User
    user = User.query.get(user_id)

    # Use DataManager to get all movies for this user through the Stargate
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', user=user, movies=movies)

# NEW: Route to handle form submission for adding a movie to a user
@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    # Extract dat from the form fields
    title = request.form.get('title')
    year = request.form.get('year')
    rating = request.form.get('rating')

    if title and year and rating:
        # Create a new Movie object from our models
        from models import Movie
        new_movie = Movie(title=title, year=int(year), rating=float(rating), user_id=user_id)
        # Send it to the DataManager to save it
        data_manager.add_movie(new_movie)

    # Redirect back to the user's movie list page
    return redirect(url_for('list_user_movies', user_id=user_id))




# Create database tables and run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Generates the tables inside movies.db if they don't exist yet
    app.run(debug=True)