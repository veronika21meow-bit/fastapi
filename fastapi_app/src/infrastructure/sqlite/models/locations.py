from infrastructure.sqlite.database import Base
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Location(Base):
    __tablename__ = "locations"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    is_published: Mapped[bool] = mapped_column(nullable=False)
    create_at: Mapped[datetime] = mapped_column(nullable=False)
