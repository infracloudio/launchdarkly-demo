from urllib.parse import urlparse
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.db import db
from app.models import User

core = Blueprint("core", __name__)


@core.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("core.fashion"))

    return render_template('index.html')


@core.route('/fashion')
@login_required
def fashion():
    return render_template('shop-fashion.html')


@core.route('/electronics')
@login_required
def electronics():
    return render_template('shop-electronic.html')


@core.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@core.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    if request.method == "POST":
        user = User(email=request.form["userEmail"])
        if User.query.filter_by(email=request.form["userEmail"]).first() is not None:
            flash("Email is already taken. Please choose another email")
            return redirect(url_for("core.register"))
        if request.form["inputPassword"] != request.form["confirmPassword"]:
            flash("Passwords must match")
            return redirect(url_for("core.register"))

        user.set_password(request.form["inputPassword"])

        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        login_user(user)
        return redirect(url_for("core.dashboard"))
    return render_template('register.html')


@core.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        flash("you're authenticated")
        return redirect(url_for("core.dashboard"))
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["userEmail"]).first()
        if user is None or not user.check_password(request.form["inputPassword"]):
            flash("Invalid username or password")
            return redirect(url_for("core.index"))
        login_user(user)

        next_page = request.args.get("next")
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("core.dashboard")
        return redirect(next_page)
    return render_template("login.html", title="Sign In")


@core.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# API's
