from flask import Flask
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import os
from .db import init_app, init_db
from . import main
load_dotenv()

def create_app():
    app = Flask(__name__)
    with app.app_context():
        init_db()
        init_app(app)
    app.secret_key = os.getenv('SECRET_APP', 'noneAZERTY')
    CSRFProtect(app)
    app.register_blueprint(main.bp)
    return app


app = create_app()

