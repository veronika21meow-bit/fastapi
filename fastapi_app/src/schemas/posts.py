from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PostRequestSchema(BaseModel):
    author_id: int = Field(..., description="ID автора поста")
    text: str = Field(..., max_length=80, description="Текст поста")
    title: Optional[str] = Field(None, max_length=256, description="Заголовок поста")
    image: Optional[str] = Field(None, description="Ссылка на изображение")
    is_published: bool = Field(True, description="Опубликовано или нет")
    location_id: Optional[int] = Field(None, description="ID местоположения")
    category_id: Optional[int] = Field(None, description="ID категории")
    pub_date: Optional[datetime] = Field(None, description="Дата публикации")


class PostResponseSchema(BaseModel):
    id: int = Field(..., description="ID поста")
    post_text: str = Field(..., description="Текст поста")
    author_name: str = Field(..., description="Имя автора")
    author_id: int = Field(..., description="ID автора")
    title: Optional[str] = Field(None, description="Заголовок поста")
    image: Optional[str] = Field(None, description="Ссылка на изображение")
    is_published: bool = Field(..., description="Опубликовано или нет")
    created_at: datetime = Field(..., description="Дата создания")
    pub_date: Optional[datetime] = Field(None, description="Дата публикации")
    
    class Config:
        from_attributes = True
