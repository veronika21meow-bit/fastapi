from typing import List, Type

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from application.infrastructure.postgres.models.comments import Comment
from application.infrastructure.postgres.models.posts import Post
from application.infrastructure.postgres.models.users import User
from application.schemas.comments import BaseComment as CreateComment
from application.schemas.comments import UpdateComment


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment
        self._author_model: Type[User] = User
        self._post_model: Type[Post] = Post

    async def get_comment_by_id(self, session: AsyncSession, id: int) -> Comment:
        query = select(self._model).where(self._model.id == id)
        comment = await session.scalar(query)
        if not comment:
            raise CommentNotFoundException()
        return comment

    async def get_comments_by_post(
        self, session: AsyncSession, post_id: int
    ) -> List[Comment]:
        post_query = select(self._post_model).where(self._post_model.id == post_id)
        post = await session.scalar(post_query)
        if not post:
            raise PostNotFoundException()
        query = select(self._model).where(self._model.post_id == post_id)
        result = await session.execute(query)
        comments = result.scalars().all()
        return comments

    async def delete_comment(self, session: AsyncSession, comment_id: int) -> None:
        comment = await self.get_comment_by_id(session, comment_id)
        await session.delete(comment)

    async def create_comment(
        self, session: AsyncSession, comment_data: CreateComment
    ) -> Comment:
        comment_dict = comment_data.model_dump(exclude_none=True)
        query = insert(self._model).values(comment_dict).returning(self._model)
        try:
            comment = await session.scalar(query)
            return comment
        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e).lower()
            if "fk_comments_author_id" in error_msg:
                raise UserNotFoundException()
            elif "fk_comments_post_id" in error_msg:
                raise PostNotFoundException()
            raise

    async def update_comment(
        self, session: AsyncSession, comment_id: int, comment_data: UpdateComment
    ) -> Comment:
        update_data = comment_data.model_dump(exclude_unset=True, exclude_none=True)
        if not update_data:
            comment = await self.get_comment_by_id(session, comment_id)
            return comment
        query = (
            update(self._model)
            .where(self._model.id == comment_id)
            .values(update_data)
            .returning(self._model)
        )
        comment = await session.scalar(query)
        if not comment:
            raise CommentNotFoundException()
        return comment

    async def add_comment_images(
        self, session: AsyncSession, comment_id: int, image_paths: list
    ) -> Comment:
        comment = await self.get_comment_by_id(session, comment_id)
        current_images = comment.images or []
        current_images.extend(image_paths)
        query = (
            update(self._model)
            .where(self._model.id == comment_id)
            .values(images=current_images)
            .returning(self._model)
        )
        updated_comment = await session.scalar(query)
        if not updated_comment:
            raise CommentNotFoundException()
        return updated_comment


    async def update_comment_images(
        self, session: AsyncSession, comment_id: int, images: list
    ) -> Comment:
        query = (
            update(self._model)
            .where(self._model.id == comment_id)
            .values(images=images)
            .returning(self._model)
        )
        updated_comment = await session.scalar(query)
        if not updated_comment:
            raise CommentNotFoundException()
        return updated_comment


    async def get_comment_images(
        self, session: AsyncSession, comment_id: int
    ) -> list:
        comment = await self.get_comment_by_id(session, comment_id)
        return comment.images