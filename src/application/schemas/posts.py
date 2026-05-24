from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import List


class BasePost(BaseModel):
    title: str = Field(..., description='Заголовок', max_length=256)
    text: str = Field(..., description='Текст')
    images: List[str] = Field(default_factory=list, description="Список изображений")    
    pub_date: datetime = Field(description=
        'Дата публикации. Если установить дату и время '
        'в будущем — можно делать отложенные публикации.'
    )
    author_id: int = Field(..., description='Автор публикации')
    location_id: int | None = Field(None, description='Местоположение')
    category_id: int | None = Field(None, description='Категория')
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')
    create_at: datetime = Field(..., description='Добавлено')


class Post(BasePost):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UpdatePost(BaseModel):
    title: str = Field(..., description='Заголовок', max_length=256)
    text: str = Field(..., description='Текст')
    images: List[str] = Field(default_factory=list, description="Список изображений")
    category_id: int | None = Field(None, description='Категория')
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')


class PostImageResponse(BaseModel):
    image: str