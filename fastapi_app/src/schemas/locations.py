from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Location(BaseModel):
    name: str = Field(..., description='Заголовок', max_length=256)
    is_published: bool = Field(..., description='Опубликовано. Снимите галочку, чтобы скрыть публикацию.')
    create_at: datetime = Field(..., description='Добавлено')


class CreateLocation(BaseModel):
    id: int
    
    model_config = ConfigDict(from_attributes=True)