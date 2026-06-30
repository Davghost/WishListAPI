from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from spectree import SpecTree
from flask_jwt_extended import JWTManager, SecurityScheme

db = SQLAlchemy()
migrate = Migrate()
api = SpecTree("flask",
    title="WishListAPI",
    version="v.1.0",
    path="docs",
    security_schemes=[
        SecurityScheme(
            name="api_key",
            data={"type": "apiKey", "name": "Authorization", "in": "header"},
        )
    ],
    security={"api_key": []},
)
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt.init_app(app)
    db.init_app(app)

    from models import WishlistItem, User, Wishlist

    migrate.init_app(app, db)

    from controllers import wishlist_controller, user_controller, wishlists_controller
    app.register_blueprint(wishlist_controller)
    app.register_blueprint(wishlists_controller)
    app.register_blueprint(user_controller)

    api.register(app)

    @app.get("/")
    def home():
        return "Hello, World"

    return app