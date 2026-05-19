import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    PostNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    PostNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository
from application.schemas.posts import Post, UpdatePost

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, post_data: UpdatePost) -> Post:
        async with self._database.session() as session:
            try:
                post = await self._repo.update_post(
                    session=session, post_id=post_id, post_data=post_data
                )
                await session.commit()
                await session.refresh(post)
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
            except CategoryNotFoundException:
                if post_data.category_id is not None:
                    error = CategoryNotFoundByIdException(id=post_data.category_id)
                    logger.error(error.get_detail())
                    raise error
                error = CategoryNotFoundException()
                logger.error(error.get_detail())
                raise error

            return Post.model_validate(obj=post)
