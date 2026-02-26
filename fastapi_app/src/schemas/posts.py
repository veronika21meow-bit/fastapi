from pydantic import BaseModel, Field
from datetime import datetime
from schemas.users import User
from schemas.locations import Location
from schemas.categories import Category



class Post(BaseModel):
    title: str = Field(..., description='Заголовок', max_length=256)
    text: str = Field(..., description='Текст')
    image: str = Field(description="Ссылка на изображение")
    pup_date: datetime = Field(description=
        'Дата публикации. Если установить дату и время '
        'в будущем — можно делать отложенные публикации.'
    )
    author: User = Field(..., description='Автор публикации')
    location: Location = Field(description='Местоположение')
    category: Category = Field(description='Категория')
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')
    create_at: datetime = Field(..., description='Добавлено')


