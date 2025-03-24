from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .core import Base


class BaseAccount(Base):

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    def to_schema(self):
        pass