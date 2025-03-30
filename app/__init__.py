from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user , logout_user , login_required
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.settings.Config')
    app.config["SECRET_KEY"] = "supersecretkey"

    db.init_app(app)
    login_manager.init_app(app)

    
    return app