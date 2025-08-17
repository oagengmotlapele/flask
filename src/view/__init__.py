from datetime import timedelta

from flask import Flask
from src.view.blueprint import auth, errors, index
from dotenv import load_dotenv
load_dotenv()

import os

def create_app():
    app = Flask(__name__)  # Keep Flask app initialization

    # Register blueprints
    app.register_blueprint(index.index)
    app.register_blueprint(auth.auth, url_prefix='/auth')
    app.register_blueprint(errors.errors)
    app.secret_key = os.getenv('app_secrect')
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE= True if os.getenv("production") == 'True' else False,
        SESSION_COOKIE_SAMESITE="Strict",
        SESSION_REFRESH_EACH_REQUEST=True,
        WTF_CSRF_TIME_LIMIT=None,
        SESSION_USE_SIGNER = True
    )

    return app

