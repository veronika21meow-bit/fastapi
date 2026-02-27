from pydantic import BaseModel, Field
from datetime import datetime


class Location(BaseModel):
    id: int
    name: str = Field(..., description='Заголовок', max_length=256)
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')
    create_at: datetime = Field(..., description='Добавлено')


