import os
from flask import Flask
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

# Base test route
@app.route('/')
def home():
    return "Welcome to MoviWeb App!"

@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)  # Temporarily returning users as a string


# Create database tables and run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Generates the tables inside movies.db if they don't exist yet
    app.run(debug=True)