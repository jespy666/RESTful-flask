import os

from dataclasses import dataclass, fields
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(slots=True)
class AppConfig:

    secret_key: str = None

    def __post_init__(self) -> None:
        load_dotenv()
        # load secret key from .env
        self.secret_key = os.getenv('SECRET_KEY')

    @staticmethod
    def get_connection_uri() -> str:
        # The environment setting up by provided ENV variable from .env
        match os.getenv('ENV', 'dev'):
            case e if e == 'dev':
                # using SQLITE for development (migration, run)
                return f'sqlite:///{BASE_DIR}/dev.db'
            case e if e == 'prod':
                # using MySQL in production
                return (
                    f"mysql://{os.getenv('DB_USER')}:"
                    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
                    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
                )
            # raise Error if invalid ENV variable
            case _:
                raise ValueError('Non-existed environment')

    def get_app_config(self) -> dict:
        # Set up Flask app
        return {
            field.name.upper(): getattr(self, field.name)
            for field in fields(self)
        }
