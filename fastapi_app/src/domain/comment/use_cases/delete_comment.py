from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from core.exceptions.database_exceptions import CommentNotFoundException
from core.exceptions.domain_exceptions import CommentNotFoundByIdException

class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> None:
        with self._database.session() as session:
            try:
                self._repo.delete_comment(session=session, comment_id=comment_id)
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                raise error