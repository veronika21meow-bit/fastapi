import logging

from application.core.exceptions.database_exceptions import PostNotFoundException
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException
from application.schemas.posts import Post
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository

logger = logging.getLogger(__name__)


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> Post:
        async with self._database.session() as session:
            try:
                post = await self._repo.get_post_by_id(session, post_id)
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error

            return Post.model_validate(obj=post)
