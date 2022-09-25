import logging
import os

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
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ld-demo.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config["LD_CLIENT_KEY"] = os.environ['LD_CLIENT_KEY']
    logging.info(app.config["LD_CLIENT_KEY"])
    app.config["LD_FRONTEND_KEY"] = os.environ['LD_FRONTEND_KEY']
    logging.info(app.config["LD_FRONTEND_KEY"])

    app.ldclient = setup_ld_client(app)

    db.init_app(app)

    from app.routes import core

    app.register_blueprint(core)
    login_manager.init_app(app)

    with app.app_context():
        from app.models import User
        db.create_all()

    migrate = Migrate(app, db)

    @app.before_request
    def setLoggingLevel():
        from flask import request

        logLevel = app.ldclient.variation(
            "set-logging-level", get_ld_non_human_user(request), logging.INFO)

        app.logger.info(f"Log level: {logLevel}")

        # set app
        app.logger.setLevel(logLevel)
        # set werkzeug
        logging.getLogger("werkzeug").setLevel(logLevel)
        # set root
        logging.getLogger().setLevel(logLevel)

    return app


@login_manager.user_loader
def load_user(id):

    from app.models import User
    return User.query.get(id)


def setup_ld_client(app) -> ldclient.LDClient:

    featureStore = InMemoryFeatureStore()
    LD_CLIENT_KEY = app.config["LD_CLIENT_KEY"]
    ld_config = LdConfig(
        sdk_key=LD_CLIENT_KEY,
        http=HTTPConfig(connect_timeout=30, read_timeout=30),
        feature_store=featureStore,
        inline_users_in_events=True
    )
    client = ldclient.LDClient(config=ld_config)
    return client


application = create_app()
