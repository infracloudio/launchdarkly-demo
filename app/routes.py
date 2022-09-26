import json
from urllib import response
from urllib.parse import urlparse
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.db import db
from app.models import User
from flask import current_app
core = Blueprint("core", __name__)


@core.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("core.fashion"))

    user = current_user.get_ld_user()
    current_flag_state = current_app.ldclient.all_flags_state(user)
    user_json = json.dumps(user)

    if current_app.ldclient.variation('redirect-to-sale', current_user.get_ld_user(), False):
        return redirect(url_for("core.sale_on"))

    return render_template('index.html', all_flags=current_flag_state.to_json_string(), user_context=user_json)


@core.route('/fashion')
@login_required
def fashion():
    user = current_user.get_ld_user()
    current_flag_state = current_app.ldclient.all_flags_state(user)
    user_json = json.dumps(user)
    return render_template('shop-fashion.html', all_flags=current_flag_state.to_json_string(), user_context=user_json)


@core.route('/electronics')
@login_required
def electronics():
    user = current_user.get_ld_user()
    current_flag_state = current_app.ldclient.all_flags_state(user)
    user_json = json.dumps(user)
    return render_template('shop-electronic.html', all_flags=current_flag_state.to_json_string(), user_context=user_json)


@core.route('/dashboard')
@login_required
def dashboard():
    user = current_user.get_ld_user()
    current_flag_state = current_app.ldclient.all_flags_state(user)
    user_json = json.dumps(user)

    liked_products = current_user.liked_products
    return render_template('dashboard.html', all_flags=current_flag_state.to_json_string(), user_context=user_json, products=json.loads(liked_products))


@core.route('/register', methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    if current_app.ldclient.variation('disable-registration', current_user.get_ld_user(), False):
        flash("Not accepting new registration, try after sometime")
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


@core.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@core.route('/sale')
def sale_on():
    user = current_user.get_ld_user()
    current_flag_state = current_app.ldclient.all_flags_state(user)
    user_json = json.dumps(user)
    return render_template('sale.html', all_flags=current_flag_state.to_json_string(), user_context=user_json)


@core.route('/add-to-like')
def add_to_like():

    if current_app.ldclient.variation('add-to-like', current_user.get_ld_user(), False):
        if len(request.args) < 1:
            return {}, 500
        max_allowed = current_app.ldclient.variation('max-like-allowed', current_user.get_ld_user(), 10)

        # add to like then
        if current_user.liked_products is None:
            current_user.liked_products = "[]"

        liked_products = json.loads(current_user.liked_products)
        if not len(liked_products) >= max_allowed:
            # do not add it to liked items
            liked_products.append(request.args.get('p'))
            current_user.liked_products = json.dumps(list(set(liked_products)))
            db.session.commit()

    return {}, 200
