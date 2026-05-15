from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.comments import CommentRepository
from application.schemas.comments import Comment
from application.core.exceptions.database_exceptions import CommentNotFoundException
from application.core.exceptions.domain_exceptions import CommentNotFoundByIdException


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> Comment:
        async with self._database.session() as session:
            try:
                comment = await self._repo.get_comment_by_id(session, comment_id)
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(comment_id=comment_id)
                raise error

            return Comment.model_validate(obj=comment)