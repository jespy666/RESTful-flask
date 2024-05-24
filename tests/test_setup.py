import os
import tempfile

from unittest import TestCase

from alembic import config, command
from sqlalchemy import func

from src.session import SessionFactory
from src.app import create_app
from src.tasks.models import Task

from tests.fixture_loader import load_fixtures

from config import BASE_DIR


class AppTestCase(TestCase):

    def setUp(self) -> None:
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.db_url = f"sqlite:///{self.db_path}"

        self.app = create_app(db_url=self.db_url).test_client()

        self.session_factory = SessionFactory(db_url=self.db_url)

        alembic_cfg = config.Config(f"{BASE_DIR}/alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", self.db_url)
        alembic_cfg.set_main_option(
            "script_location",
            f"{BASE_DIR}/migrations"
        )
        command.upgrade(alembic_cfg, "head")

        self.fill_db()

    def tearDown(self) -> None:
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def fill_db(self) -> None:
        session = self.session_factory.get_session()
        if not self.is_filled():
            db_dump = load_fixtures(f'{BASE_DIR}/tests/fixtures/tasks.json')
            for record in db_dump:
                session.add(Task(**record))
            session.commit()
        session.close()

    def clean_db(self) -> None:
        session = self.session_factory.get_session()
        session.query(Task).delete()
        session.commit()
        session.close()

    def is_filled(self) -> bool:
        session = self.session_factory.get_session()
        count = session.query(func.count(Task.id)).scalar()
        session.close()
        return count != 0
