from flask import Flask
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import os
from .db import init_app, init_db
from . import main
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_APP', 'une-cle-secrete-par-defaut'),
    )

    if test_config is not None:
        app.config.update(test_config)
    
    init_app(app) 
    CSRFProtect(app)
    app.register_blueprint(main.bp)
    return app


app = create_app()

