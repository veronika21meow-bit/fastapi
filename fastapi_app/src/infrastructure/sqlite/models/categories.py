from infrastructure.sqlite.database import Base
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    create_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
