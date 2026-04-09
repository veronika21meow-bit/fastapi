from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class BaseComment(BaseModel):
    text: str = Field(..., description='Текст комментария')
    post_id: int | None = Field(None, description='Пост')
    author_id: int = Field(..., description='Автор комментария')
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')
    create_at: datetime = Field(..., description='Добавлено')

class Comment(BaseComment):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
