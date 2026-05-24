from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


class BaseComment(BaseModel):
    text: str = Field(..., description='Текст комментария')
    post_id: int | None = Field(None, description='Пост')
    author_id: int = Field(..., description='Автор комментария')
    images: List[str] = Field(default_factory=list, description="Список изображений")    
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')
    create_at: datetime = Field(..., description='Добавлено')

class Comment(BaseComment):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class UpdateComment(BaseModel):
    text: str = Field(..., description='Текст комментария')
    images: List[str] = Field(default_factory=list, description="Список изображений")    
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')

class CommentImageResponse(BaseModel):
    image: str