import os
from flask import Flask
from dotenv import load_dotenv
 
load_dotenv()
 
 
def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "troque-esta-chave-no-env")
 
    from .routes import main
    app.register_blueprint(main)
 
    return app