from ..database import Base
from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, JSON


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    images: Mapped[List[str]] = mapped_column(JSON, nullable=True, default=list)
    pub_date: Mapped[datetime] = mapped_column(nullable=True)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    create_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    # Внешние ключи
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)
    # Связи
    author = relationship("User", back_populates="posts")
    location = relationship("Location", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
