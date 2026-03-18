from datetime import datetime
from pydantic import BaseModel, Field
from schemas.users import User
from schemas.locations import Location
from schemas.categories import Category


class Post(BaseModel):
    id: int
    title: str = Field(..., description='Заголовок', max_length=256)
    text: str = Field(..., description='Текст')
    image: str | None = Field(None, description="Ссылка на изображение")
    pub_date: datetime = Field(description=
        'Дата публикации. Если установить дату и время '
        'в будущем — можно делать отложенные публикации.'
    )
    author_id: int = Field(..., description='Автор публикации')
    location_id: int | None = Field(None, description='Местоположение')
    category_id: int | None = Field(None, description='Категория')
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')
    create_at: datetime = Field(..., description='Добавлено')
