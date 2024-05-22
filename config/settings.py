import os

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class AppConfig:
    secret_key: str
    sqlalchemy_database_uri: str

    def get_connection_uri(self) -> str:
        return self.sqlalchemy_database_uri


app_config = (
    AppConfig(
        os.getenv('SECRET_KEY'),
        f'sqlite:///{BASE_DIR}/dev.db'
    )
)
