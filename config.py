# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')  # Fallback to SQLite if not set
    SQLALCHEMY_TRACK_MODIFICATIONS = False
