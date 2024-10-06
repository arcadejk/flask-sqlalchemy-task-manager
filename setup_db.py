from taskmanager import app, db

# Set up the application context
with app.app_context():
    db.create_all()
