from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from spectree import SpecTree
from spectree.models import SecurityScheme, SecuritySchemeData, SecureType
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
api = SpecTree(
    "flask",
    title="WishListAPI",
    version="v.1.0",
    path="docs",
    security_schemes=[
        SecurityScheme(
            name="bearerAuth",
            data=SecuritySchemeData(
                type=SecureType.HTTP,
                scheme="bearer",
                bearerFormat="JWT",
                description="JWT Authorization header using the Bearer scheme",
            ),
        )
    ],
    security=[{"bearerAuth": []}],
)
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt.init_app(app)
    db.init_app(app)

    @jwt.unauthorized_loader
    def unauthorized_response(error):
        return jsonify({"id": None, "msg": "Authorization required: missing or invalid JWT."}), 401

    @jwt.invalid_token_loader
    def invalid_token_response(error):
        return jsonify({"id": None, "msg": "Invalid token: authorization failed."}), 401

    @jwt.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        return jsonify({"id": None, "msg": "Token expired: please log in again."}), 401

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