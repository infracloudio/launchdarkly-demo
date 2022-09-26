import hashlib
import time
import uuid
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from dataclasses import dataclass

from app.db import db
from flask import current_app


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        super(AnonymousUserMixin, self).__init__()

    def get_ld_user(self):
        app_version = current_app.config['VERSION']
        user = {
            "key": str(uuid.uuid1()),
            "custom": {
                "app_version": app_version
            }}

        return user
@dataclass
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    liked_products = db.Column(db.Text,default="[]")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_ld_user(self):
        milliseconds = int(round(time.time() * 1000))
        app_version = current_app.config['VERSION']
        user_key = self.get_email_hash()
        user = {
            'key': user_key,
            'email': self.email,
            "custom": {
                'app_version': app_version,
                'date': milliseconds,
            },
            'privateAttributeNames': [],
        }

        return user

    def get_email_hash(self):
        return hashlib.md5(self.email.encode()).hexdigest()

    def __repr__(self) -> str:
        return f'User: {self.email}'


@dataclass
class Products(db.Model):

    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=True)
    description = db.Column(db.String(150), index=True, nullable=True)
    price = db.Column(db.Float())
    image_url = db.Column(db.String(1000), nullable=True)
    product_type = db.Column(db.String(100))
    on_sale = db.Column(db.Boolean,default=False)
    sale_price = db.Column(db.Float())
