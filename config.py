import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


def get_env_variable(name: str, default: str | None = None, required: bool = False) -> str:
    value = os.environ.get(name, default)
    if required and (value is None or value == ""):
        raise EnvironmentError(f"The environment variable '{name}' must be set.")
    return value


class Config():
    SECRET_KEY = get_env_variable("SECRET_KEY", required=True)
    APP_TITLE = "WishListAPI"

    JWT_SECRET_KEY = get_env_variable("JWT_SECRET_KEY", required=True)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_TYPE = "Bearer"

    SQLALCHEMY_DATABASE_URI = get_env_variable(
        "DATABASE_URL",
        default="sqlite:///" + os.path.join(basedir, "app.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app():
        pass