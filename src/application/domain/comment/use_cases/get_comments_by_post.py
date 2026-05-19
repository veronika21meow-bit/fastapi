import logging
from typing import List

from application.core.exceptions.database_exceptions import PostNotFoundException
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import CommentRepository
from application.schemas.comments import Comment

logger = logging.getLogger(__name__)


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, post_id: int) -> List[Comment]:
        async with self._database.session() as session:
            try:
                comments = await self._repo.get_comments_by_post(session, post_id)
                result = []
                for comment in comments:
                    result.append(Comment.model_validate(obj=comment))
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
            return result
