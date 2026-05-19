import logging

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
    UserNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import CommentRepository
from application.schemas.comments import BaseComment as CreateComment
from application.schemas.comments import Comment

logger = logging.getLogger(__name__)


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_data: CreateComment) -> Comment:
        async with self._database.session() as session:
            try:
                comment = await self._repo.create_comment(
                    session=session, comment_data=comment_data
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=comment_data.post_id)
                logger.error(error.get_detail())
                raise error
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=comment_data.author_id)
                logger.error(error.get_detail())
                raise error

            return Comment.model_validate(obj=comment)
