from typing import List, Type

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from application.infrastructure.postgres.models.categories import Category
from application.infrastructure.postgres.models.locations import Location
from application.infrastructure.postgres.models.posts import Post
from application.infrastructure.postgres.models.users import User
from application.schemas.posts import BasePost as CreatePost
from application.schemas.posts import UpdatePost


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post
        self._author_model: Type[User] = User
        self._location_model: Type[Location] = Location
        self._category_model: Type[Category] = Category

    async def get_post_by_id(self, session: AsyncSession, id: int) -> Post:
        query = select(self._model).where(self._model.id == id)
        post = await session.scalar(query)
        if not post:
            raise PostNotFoundException()
        return post

    async def get_posts_by_author(
        self, session: AsyncSession, author_id: int
    ) -> List[Post]:
        author_query = select(self._author_model).where(
            self._author_model.id == author_id
        )
        author = await session.scalar(author_query)
        if not author:
            raise UserNotFoundException()
        query = select(self._model).where(self._model.author_id == author_id)
        result = await session.execute(query)
        posts = result.scalars().all()
        return posts

    async def get_all_posts(self, session: AsyncSession) -> List[Post]:
        query = select(self._model)
        result = await session.execute(query)
        posts = result.scalars().all()
        return posts

    async def delete_post(self, session: AsyncSession, post_id: int) -> None:
        post = await self.get_post_by_id(session, post_id)
        await session.delete(post)

    async def create_post(self, session: AsyncSession, post_data: CreatePost) -> Post:
        post_dict = post_data.model_dump(exclude_none=True)
        query = insert(self._model).values(post_dict).returning(self._model)
        try:
            post = await session.scalar(query)
            return post
        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e).lower()
            if "posts_author_id_fkey" in error_msg:
                raise UserNotFoundException()
            elif "posts_location_id_fkey" in error_msg:
                raise LocationNotFoundException()
            elif "posts_category_id_fkey" in error_msg:
                raise CategoryNotFoundException()
            raise

    async def update_post(
        self, session: AsyncSession, post_id: int, post_data: UpdatePost
    ) -> Post:
        update_data = post_data.model_dump(exclude_unset=True, exclude_none=True)
        if post_data.category_id is not None:
            category_query = select(self._category_model).where(
                self._category_model.id == post_data.category_id
            )
            category = await session.scalar(category_query)
            if not category:
                raise CategoryNotFoundException()
        query = (
            update(self._model)
            .where(self._model.id == post_id)
            .values(update_data)
            .returning(self._model)
        )
        try:
            post = await session.scalar(query)
            if not post:
                raise PostNotFoundException()
            return post
        except IntegrityError:
            raise CategoryNotFoundException()

    async def add_post_images(
        self, session: AsyncSession, post_id: int, image_paths: list
    ) -> Post:
        post = await self.get_post_by_id(session, post_id)
        current_images = post.images or []
        current_images.extend(image_paths)
        query = (
            update(self._model)
            .where(self._model.id == post_id)
            .values(images=current_images)
            .returning(self._model)
        )
        updated_post = await session.scalar(query)
        if not updated_post:
            raise PostNotFoundException()
        return updated_post

    async def update_post_images(
        self, session: AsyncSession, post_id: int, images: list
    ) -> Post:
        query = (
            update(self._model)
            .where(self._model.id == post_id)
            .values(images=images)
            .returning(self._model)
        )
        updated_post = await session.scalar(query)
        if not updated_post:
            raise PostNotFoundException()
        return updated_post

    async def get_post_images(self, session: AsyncSession, post_id: int) -> list:
        post = await self.get_post_by_id(session, post_id)
        return post.images
