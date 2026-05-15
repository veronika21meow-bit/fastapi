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
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", name="fk_comments_post_id", ondelete="SET NULL"), 
        nullable=True
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", name="fk_comments_author_id"), 
        nullable=False
    )
    
    # Связи
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
