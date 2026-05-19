import logging
from typing import List

from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exceptions import UserNotFoundByIdException
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository
from application.schemas.posts import Post

logger = logging.getLogger(__name__)


class GetPostsByAuthorUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, author_id: int) -> List[Post]:
        async with self._database.session() as session:
            try:
                posts = await self._repo.get_posts_by_author(session, author_id)
                result = []
                for post in posts:
                    result.append(Post.model_validate(obj=post))
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=author_id)
                logger.error(error.get_detail())
                raise error
            return result
