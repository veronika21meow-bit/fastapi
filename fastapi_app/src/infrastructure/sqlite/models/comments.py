from infrastructure.sqlite.database import Base
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.users import User
from models.posts import Post


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    is_published: Mapped[bool] = mapped_column(nullable=False)
    create_at: Mapped[datetime] = mapped_column(nullable=False)
    # Внешние ключи
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # Связи
    post: Mapped["Post"] = relationship("Location", back_populates="posts")
    author: Mapped["User"] = relationship("User", back_populates="posts")
