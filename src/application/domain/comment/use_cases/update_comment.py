import logging

from application.core.exceptions.database_exceptions import CommentNotFoundException
from application.core.exceptions.domain_exceptions import CommentNotFoundByIdException
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import CommentRepository
from application.schemas.comments import Comment, UpdateComment

logger = logging.getLogger(__name__)


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, comment_data: UpdateComment) -> Comment:
        async with self._database.session() as session:
            try:
                comment = await self._repo.update_comment(
                    session=session, comment_id=comment_id, comment_data=comment_data
                )
                await session.commit()
                await session.refresh(comment)
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error

            return Comment.model_validate(obj=comment)
