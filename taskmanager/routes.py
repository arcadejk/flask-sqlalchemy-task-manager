from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
import os
from taskmanager import app, db
from taskmanager.models import Category, Task, User  # Import du modèle User
from datetime import datetime  # Import pour la conversion des dates
from taskmanager.forms import PasswordResetRequestForm  # Adjusted import to match your app structure


# Configuration du dossier de téléchargement pour les fichiers envoyés
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Page d'accueil, uniquement accessible après connexion
@app.route("/")
@login_required
def home():
    tasks = list(Task.query.order_by(Task.id).all())
    return render_template("tasks.html", tasks=tasks)

# Gestion des catégories
@app.route("/categories")
@login_required
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)

@app.route("/add_category", methods=["GET", "POST"])
@login_required
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")

@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)

@app.route("/delete_category/<int:category_id>")
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))

# Ajout de tâche avec lien et fichier soumis
@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        # Convertir la chaîne de caractères 'due_date' en objet 'date'
        due_date_str = request.form.get("due_date")
        due_date = datetime.strptime(due_date_str, '%d %B, %Y').date()  # Ajuster le format si nécessaire

        # Créer la tâche avec les nouveaux champs : lien et fichier soumis
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=bool(request.form.get("is_urgent")),  # Convertir en booléen
            due_date=due_date,  # Utiliser l'objet 'date' ici
            link=request.form.get("link"),  # Nouveau champ pour le lien
            submitted_file=None,  # Placeholder pour le fichier envoyé
            category_id=int(request.form.get("category_id")),  # Convertir category_id en entier
            user_id=current_user.id  # Associer la tâche à l'utilisateur connecté
        )

        # Gestion de l'envoi de fichier
        if 'submitted_file' in request.files:
            file = request.files['submitted_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                task.submitted_file = filename

        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html", categories=categories)

# Routes pour le login et logout
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Basic validation (password matching, user existence, etc.)
        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "error")
            return redirect(url_for('register'))
        
        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Un utilisateur avec cet e-mail existe déjà.", "error")
            return redirect(url_for('register'))
        
        # Create a new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Assuming the `User` model has a method to hash the password
        db.session.add(new_user)
        db.session.commit()

        # Flash message for successful registration
        flash("Compte créé avec succès ! Vous pouvez maintenant vous connecter.", "success")

        # Redirect to the login page
        return redirect(url_for('login'))

    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()

        # Check if user exists and if password matches
        if user and user.check_password(password):  # Assuming `check_password` verifies the hashed password
            login_user(user)
            flash("Connexion réussie !", "success")
            return redirect(url_for("home"))  # Redirect to home page upon successful login
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.", "error")
            return redirect(url_for("login"))  # Stay on login page if login fails

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("login"))

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Logic to send a reset password email (you need to implement this)
            flash("Un lien de réinitialisation de mot de passe a été envoyé à votre adresse email.", "info")
        else:
            flash("Aucun compte trouvé avec cette adresse email.", "error")
        return redirect(url_for("login"))
    return render_template("reset_password.html", form=form)
