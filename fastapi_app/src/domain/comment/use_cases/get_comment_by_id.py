from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import Comment
from core.exceptions.database_exceptions import CommentNotFoundException
from core.exceptions.domain_exceptions import CommentNotFoundByIdException


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> Comment:
        with self._database.session() as session:
            try:
                comment = self._repo.get_comment_by_id(session, comment_id)
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(comment_id=comment_id)
                raise error

            return Comment.model_validate(obj=comment)