from flask import Flask


def create_app():
    app = Flask(__name__)
    from app.routes import core
    app.register_blueprint(core)
    
    return app

application = create_app()