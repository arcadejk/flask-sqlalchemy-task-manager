import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from markupsafe import escape

# Optional: Only if env.py is used to set environment variables
if os.path.exists("env.py"):
    import env  # noqa

# Initialize Flask application
app = Flask(__name__)

# Set up database configuration conditionally based on the environment
if os.environ.get("ENV") == "production":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL")  # Production database URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Development SQLite database

# Ensure SECRET_KEY is set (required for sessions and security)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set up Flask-Login for user authentication management
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view if the user is not logged in
login_manager.login_message_category = 'info'  # Optional: Category for flashed messages

# Ensure the User model is correctly loaded by Flask-Login
from taskmanager.models import User  # noqa

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes (ensure taskmanager/routes.py exists)
from taskmanager import routes  # noqa

# Run the application if executed directly
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "127.0.0.1"), 
        port=int(os.environ.get("PORT", 5000)), 
        debug=os.environ.get("DEBUG", False)
    )

from flask_mail import Mail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Example using Gmail
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Your email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Your email password

mail = Mail(app)
