from typing import Type, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.infrastructure.postgres.models.comments import Comment
from application.infrastructure.postgres.models.users import User
from application.infrastructure.postgres.models.posts import Post
from application.schemas.comments import BaseComment as CreateComment, UpdateComment
from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException
)

class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment
        self._author_model: Type[User] = User
        self._post_model: Type[Post] = Post

    async def get_comment_by_id(self, session: AsyncSession, id: int) -> Comment:
        query = select(self._model).where(self._model.id == id)
        result = await session.execute(query)
        comment = result.scalar_one_or_none()

        if not comment:
            raise CommentNotFoundException()

        return comment
    
    async def get_comments_by_post(self, session: AsyncSession, post_id: int) -> List[Comment]:
        post_query = select(self._post_model).where(
            self._post_model.id == post_id
        )
        post_result = await session.execute(post_query)
        post = post_result.scalar_one_or_none()
        if not post:
            raise PostNotFoundException()
        query = select(self._model).where(self._model.post_id == post_id)
        result = await session.execute(query)
        comments = result.scalars().all()
        return comments

    async def delete_comment(self, session: AsyncSession, comment_id: int) -> None:
        comment = await self.get_comment_by_id(session, comment_id)
        if comment:
            await session.delete(comment)
        else:
            raise CommentNotFoundException()
    
    async def create_comment(self, session:AsyncSession, comment_data: CreateComment) -> Comment:
        author_query = select(self._author_model).where(self._author_model.id == comment_data.author_id)
        author_result = await session.execute(author_query)
        author = author_result.scalar_one_or_none()
        
        if not author:
            raise UserNotFoundException()

        post_query = select(self._post_model).where(self._post_model.id == comment_data.post_id)
        post_result = await session.execute(post_query)
        post = post_result.scalar_one_or_none()
        
        if not post:
            raise PostNotFoundException()

        data = comment_data.model_dump(exclude_none=True)
        comment = self._model(**data)
        session.add(comment)
        await session.flush()
        await session.refresh(comment)

        return comment
    
    async def update_comment(self, session:AsyncSession, comment_id: int, comment_data: UpdateComment) -> Comment:
        comment = await self.get_comment_by_id(session, comment_id)
        update_data = comment_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(comment, key, value)
        await session.flush()
        await session.refresh(comment)
        return comment
