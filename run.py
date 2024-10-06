import os
from taskmanager import app, db

# Main function
if __name__ == "__main__":
    # Create database tables within the app context
    with app.app_context():
        db.create_all()

    # Run the app with environment-specific configurations
    app.run(
        host=os.environ.get("IP", "127.0.0.1"),
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("DEBUG", False)
    )
