import os

class Config:
    SECRET_KEY = 'your_secret_key'  # Make sure to change this to a strong secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # SQLite database URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')  # Image upload folder
