from pydantic import BaseModel, SecretStr, Field, EmailStr
from schemas.posts import Post
from schemas.users import User
from datetime import datetime


class Comment(BaseModel):
    text: str = Field(..., description='Текст комментария')
    post: Post = Field(..., description='Пост')
    author: User = Field(..., description='Автор комментария')
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')
    created_at: datetime = Field(..., description='Добавлено')
