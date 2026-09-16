import os


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

if os.environ.get("VERCEL"):
    INSTANCE_DIR = "/tmp/instance"
else:
    INSTANCE_DIR = os.path.join(
        BASE_DIR,
        "instance"
    )

os.makedirs(
    INSTANCE_DIR,
    exist_ok=True
)


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "development-jwt-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(
            INSTANCE_DIR,
            "surplus_food.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
