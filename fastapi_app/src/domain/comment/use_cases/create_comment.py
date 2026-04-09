from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository


from schemas.comments import Comment, BaseComment as CreateComment
from core.exceptions.database_exceptions import (
    PostNotFoundException,
    UserNotFoundException
)
from core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserNotFoundByIdException
)

class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_data) -> Comment:
        with self._database.session() as session:
            try:
                comment = self._repo.create_comment(session=session, comment_data=comment_data)
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=comment_data.post_id)
                raise error
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=comment_data.author_id)
                raise error

            return Comment.model_validate(obj=comment)