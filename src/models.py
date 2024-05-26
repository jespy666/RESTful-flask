from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr
)


class Base(DeclarativeBase):

    __abstract__ = True

    @declared_attr.directive
    # set up table name automatically
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    # set default primary key for all tables
    id: Mapped[int] = mapped_column(primary_key=True)
