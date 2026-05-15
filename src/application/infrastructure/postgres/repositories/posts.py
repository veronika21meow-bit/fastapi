from typing import Type, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.infrastructure.postgres.models.posts import Post
from application.infrastructure.postgres.models.users import User
from application.infrastructure.postgres.models.locations import Location
from application.infrastructure.postgres.models.categories import Category
from application.schemas.posts import BasePost as CreatePost, UpdatePost
from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException 
)


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post
        self._author_model: Type[User] = User
        self._location_model: Type[Location] = Location
        self._category_model: Type[Category] = Category
    async def get_post_by_id(self, session: AsyncSession, id: int) -> Post | None:
        query = select(self._model).where(self._model.id == id)
        result = await session.execute(query)
        post = result.scalar_one_or_none()
        if not post:
            raise PostNotFoundException()
        return post
    
    async def get_posts_by_author(self, session: AsyncSession, author_id: int) -> List[Post]:
        query = (
            select(self._model)
            .where(self._model.author_id == author_id)
        )
        posts = query.all()
        return posts
    
    async def get_all_posts(self, session: AsyncSession) -> List[Post]:
        query = select(self._model)
        result = await session.execute(query)
        posts = result.scalars().all()
        return posts

    
    async def delete_post(self, session: AsyncSession, post_id: int) -> None:
        post = await self.get_post_by_id(session, post_id)
        if post:
            await session.delete(post)
        else:
            raise PostNotFoundException()
    
    async def create_post(self, session:AsyncSession, post_data: CreatePost) -> Post:
        author_query = select(self._author_model).where(self._author_model.id == post_data.author_id)
        author_result = await session.execute(author_query)
        author = author_result.scalar_one_or_none()
        
        if not author:
            raise UserNotFoundException()

        if post_data.location_id is not None:
            location_query = select(self._location_model).where(self._location_model.id == post_data.location_id)
            location_result = await session.execute(location_query)
            location = location_result.scalar_one_or_none()
            if not location:
                raise LocationNotFoundException()

        if post_data.category_id is not None:
            category_query = select(self._category_model).where(self._category_model.id == post_data.category_id)
            category_result = await session.execute(category_query)
            category = category_result.scalar_one_or_none()
            if not category:
                raise CategoryNotFoundException()

        post_data = post_data.model_dump(exclude_none=True)
        post = self._model(**post_data)
        session.add(post)
        await session.flush()
        await session.refresh(post)

        return post
    
    async def update_post(self, session:AsyncSession, id: int, title: str, 
                    text: str, is_published: bool = True, category_id: int | None = None,
                    image: str | None = None) -> Post:
        post = self.get_post_by_id(session, id)
        if post:
            post.title=title
            post.text = text
            post.is_published = is_published
            post.category_id = category_id
            post.image = image
            session.commit()
        return post
