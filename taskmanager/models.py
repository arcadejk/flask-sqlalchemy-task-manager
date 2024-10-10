from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from taskmanager import db

class User(db.Model, UserMixin):
    """User model for storing user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hashes the password and stores it in the database."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hashed password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Representation of the User model."""
        return f'<User {self.username}>'


class Category(db.Model):
    """Schema for the Category model."""
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False)
    tasks = db.relationship("Task", backref="category", cascade="all, delete", lazy=True)

    def __repr__(self):
        """Representation of the Category model."""
        return self.category_name


class Task(db.Model):
    """Schema for the Task model."""
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        """Representation of the Task model."""
        return f"#{self.id} - Task: {self.task_name} | Urgent: {self.is_urgent}"
