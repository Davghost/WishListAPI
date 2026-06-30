import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY=os.environ.get("SECRET_KEY")
    APP_TITLE="WishListAPI"

    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers"]

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app():
        pass