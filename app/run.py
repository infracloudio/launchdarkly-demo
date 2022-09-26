import logging
import os
import subprocess

import ldclient
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from ldclient import Config as LdConfig
from ldclient.client import HTTPConfig
from ldclient.feature_store import CacheConfig, InMemoryFeatureStore

from app.db import db
from app.util import get_ld_non_human_user

login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    
    VERSION = subprocess.check_output(["git", "log", "-1", "--pretty=%h"]).decode('utf-8').rstrip()
    app.config['VERSION'] = VERSION
    app.logger.info(f"App Version Running: {VERSION}")
    app.secret_key = "2093nifoskh@324%fiafaf/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ld-demo.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config["LD_SDK_KEY"] = os.environ['LD_SDK_KEY']
    app.logger.info(f'SDK Key: {app.config["LD_SDK_KEY"]}')
    app.config["LD_FRONTEND_KEY"] = os.environ['LD_FRONTEND_KEY']
    app.logger.info(f'Client Key: {app.config["LD_FRONTEND_KEY"]}')

    app.ldclient = setup_ld_client(app)

    db.init_app(app)

    from app.routes import core
    from app.api import api
    from app.models import AnonymousUser



    app.register_blueprint(core)
    app.register_blueprint(api,url_prefix='/api')

    login_manager.init_app(app)
    login_manager.login_view = "core.index"
    login_manager.anonymous_user = AnonymousUser

    with app.app_context():
        from app.models import User, Products
        db.create_all()
        
        if not len(Products.query.all()):
            p1 = Products(
                name='Iphone XR',
                description='Best Iphone at this price',
                price=999,
                image_url="https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg",
                product_type="electronics",
                on_sale=False,
                sale_price=699
                    )

            p2 = Products(
                name='Headphone',
                description='',
                price=400,
                image_url="https://images.pexels.com/photos/205926/pexels-photo-205926.jpeg",
                product_type="electronics",
                on_sale=True,
                sale_price=200
            )

            p3 = Products(
                name='Game Controller',
                description='',
                price=700,
                image_url="https://images.pexels.com/photos/1298601/pexels-photo-1298601.jpeg",
                product_type="electronics",
                on_sale=False,
                sale_price=500
            )

            p4 = Products(
                name='Apple Watch 6',
                description='',
                price=999,
                image_url="https://images.pexels.com/photos/393047/pexels-photo-393047.jpeg",
                product_type="electronics",
                on_sale=True,
                sale_price=700
            )


            p5 = Products(
                name='Coat',
                description='Best Iphone at this price',
                price=20,
                image_url="https://images.pexels.com/photos/157675/fashion-men-s-individuality-black-and-white-157675.jpeg",
                product_type="fashion",
                on_sale=False,
                sale_price=15
                    )

            p6 = Products(
                name='Yellow Hoodie',
                description='',
                price=50,
                image_url="https://images.pexels.com/photos/1183266/pexels-photo-1183266.jpeg",
                product_type="fashion",
                on_sale=True,
                sale_price=40
            )

            p7 = Products(
                name='Offwhite T-Shirt',
                description='',
                price=30,
                image_url="https://images.pexels.com/photos/428340/pexels-photo-428340.jpeg",
                product_type="fashion",
                on_sale=False,
                sale_price=15
            )

            p8 = Products(
                name='Nike Shoe',
                description='',
                price=50,
                image_url="https://images.pexels.com/photos/3193731/pexels-photo-3193731.jpeg",
                product_type="fashion",
                on_sale=True,
                sale_price=47
            )
            
            db.session.add(p1)
            db.session.add(p2)
            db.session.add(p3)
            db.session.add(p4)
            db.session.add(p5)
            db.session.add(p6)
            db.session.add(p7)
            db.session.add(p8)
            db.session.commit()

    migrate = Migrate(app, db)

    @app.before_request
    def setLoggingLevel():
        from flask import request

        logLevel = app.ldclient.variation(
            "set-logging-level", get_ld_non_human_user(request), logging.INFO)

        app.logger.info(f"Log level: {logLevel}")

        app.logger.setLevel(logLevel)
        logging.getLogger("werkzeug").setLevel(logLevel)
        logging.getLogger().setLevel(logLevel)

    return app


@login_manager.user_loader
def load_user(id):

    from app.models import User
    return User.query.get(id)


def setup_ld_client(app) -> ldclient.LDClient:

    featureStore = InMemoryFeatureStore()
    LD_SDK_KEY = app.config["LD_SDK_KEY"]
    LD_FRONTEND_KEY = app.config["LD_FRONTEND_KEY"]
    ld_config = LdConfig(
        sdk_key=LD_SDK_KEY,
        http=HTTPConfig(connect_timeout=30, read_timeout=30),
        feature_store=featureStore,
        inline_users_in_events=True
    )
    client = ldclient.LDClient(config=ld_config)
    return client


application = create_app()
