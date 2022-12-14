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
from app.util import get_ld_non_human_user, load_products

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

    from app.api import api
    from app.models import AnonymousUser, ma
    from app.routes import core
    



    app.register_blueprint(core)
    app.register_blueprint(api,url_prefix='/api')

    login_manager.init_app(app)
    login_manager.login_view = "core.index"
    login_manager.anonymous_user = AnonymousUser
    
    ma.init_app(app)

    with app.app_context():
        from app.models import Products, User
        db.create_all()
        if not len(Products.query.all()):
            load_products()
            
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
