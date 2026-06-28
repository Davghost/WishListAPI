from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from spectree import SpecTree

db = SQLAlchemy()
migrate = Migrate()
api = SpecTree("flask", title="WishListAPI", version="v.1.0", path="docs")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from models import WishlistItem

    migrate.init_app(app, db)

    from controllers import wishlist_controller
    app.register_blueprint(wishlist_controller)

    api.register(app)

    @app.get("/")
    def home():
        return "Hello, World"

    return app