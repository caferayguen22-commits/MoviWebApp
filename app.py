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

# DUMMY ROUTE: Just so url_for('list_user_movies') in HTML doesn't crash right now
@app.route('/users/<int:user_id>')
def list_user_movies(user_id):
    return f"Future movie list for user {user_id}"



# Create database tables and run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Generates the tables inside movies.db if they don't exist yet
    app.run(debug=True)