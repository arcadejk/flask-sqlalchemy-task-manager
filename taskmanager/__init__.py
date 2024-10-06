import os
from flask import Flask
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Optional: Only if env.py is used to set environment variables
if os.path.exists("env.py"):
    import env  # noqa

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "127.0.0.1"), 
    port=int(os.environ.get("PORT", 5000)), 
    debug=os.environ.get("DEBUG", False)
    )


# Set up database configuration conditionally based on environment
if os.environ.get("ENV") == "production":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL")  # Use production database URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for development

# Ensure SECRET_KEY is set
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Make sure taskmanager/routes.py exists
from taskmanager import routes  # noqa
