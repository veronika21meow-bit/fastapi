from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class BaseCategory(BaseModel):
    id: int
    title: str = Field(..., description='Заголовок', max_length=256)
    description: str = Field(..., description='Описание')
    slug: str = Field(...,
                      description=(
                          'Идентификатор. Идентификатор '
                          'страницы для URL; разрешены символы '
                          'латиницы, цифры, дефис и подчёркивание.'))
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')
    create_at: datetime = Field(..., description='Добавлено')


class Category(BaseCategory):
    id: int

    model_config = ConfigDict(from_attributes=True)



