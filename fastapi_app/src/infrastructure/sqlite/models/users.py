from infrastructure.sqlite.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    