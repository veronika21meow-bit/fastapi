from pydantic import BaseModel, SecretStr, Field, EmailStr
from schemas.posts import Post
from schemas.users import User
from datetime import datetime


class Comment(BaseModel):
    id: int
    text: str = Field(..., description='Текст комментария')
    post_id: int = Field(..., description='Пост')
    author_id: int = Field(..., description='Автор комментария')
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')
    create_at: datetime = Field(..., description='Добавлено')
