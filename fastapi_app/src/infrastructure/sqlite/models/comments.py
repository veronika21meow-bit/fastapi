from ..database import Base
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    text: Mapped[str] = mapped_column(nullable=False)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    create_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    # Внешние ключи
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # Связи
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
