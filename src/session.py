from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session



class SessionFactory:

    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_session(self) -> Session:
        with self.session_factory() as session:
            return session
