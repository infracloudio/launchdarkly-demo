from app.auth_middleware import token_required
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
import jwt
from app.db import db
from app.models import Products, User
from flask import current_app, jsonify

api = Blueprint("api", __name__)


@api.route("/login", methods=["POST"])
def login():
    try:
        data = request.json

        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400

        user = User.query.filter_by(email=data["email"]).first()
        if user is None or not user.check_password(data["password"]):
            return {
                "message": "Error fetching auth token!, invalid email or password",
                "data": None,
                "error": "Unauthorized"
            }, 404
        else:
            try:
                # token should expire after 24 hrs
                user = user.get_ld_user()
                user["token"] = jwt.encode({"user_id": user['email']},
                                           current_app.config["SECRET_KEY"],
                                           algorithm="HS256"
                                           )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong! Unable to create token",
                    "message": str(e)
                }, 500
    except Exception as e:
        return {
            "message": "Something went wrong! Check parameters",
            "error": str(e),
            "data": None
        }, 500


@api.route('/electronics', methods=['GET'])
@token_required
def list_electronics(current_user):
    try:
        books = Products.query.all()
        return jsonify({
            "message": "successfully retrieved all products",
            "data": books
        })
    except Exception as e:
        current_app.logger.debug(e, exc_info=True)
        return jsonify({
            "message": "failed to retrieve all products",
            "error": str(e),
            "data": None
        }), 500
