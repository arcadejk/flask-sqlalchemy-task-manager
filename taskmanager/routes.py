from flask import render_template
from taskmanager import app, db
from markupsafe import escape
from taskmanager.models import Category, Task


@app.route("/")
def home():
    return render_template("base.html")