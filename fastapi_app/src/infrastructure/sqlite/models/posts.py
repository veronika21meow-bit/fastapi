from infrastructure.sqlite.database import Base
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from models.users import User
from models.locations import Location
from models.categories import Category



class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=True)
    pup_date: Mapped[datetime] = mapped_column(nullable=True)
    is_published: Mapped[bool] = mapped_column(nullable=False)
    create_at: Mapped[datetime] = mapped_column(nullable=False)
    # Внешние ключи
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)
    # Связи
    author: Mapped["User"] = relationship("User", back_populates="posts")
    location: Mapped["Location"] = relationship("Location", back_populates="posts")
    category: Mapped["Category"] = relationship("Category", back_populates="posts")

