from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from ..models import Base


class Task(Base):

    title: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(250),
        nullable=True,
        unique=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        unique=False,
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        unique=False,
        default=None,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description if self.description else '',
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else ''  # noqa: E501
        }
