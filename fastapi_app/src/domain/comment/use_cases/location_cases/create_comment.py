from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.comments import Comment as CommentSchema


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UserRepository()

    async def execute(self, text: str, author_id: int,
                      post_id: int, is_published: bool = True) -> CommentSchema:
        with self._database.session() as session:

            comment = self._repo.create_comment(
                session=session,
                text=text,
                author_id=author_id,
                post_id=post_id,
                is_published=is_published
            )

            comment_dict = {
                "id": comment.id,
                "text": comment.text,
                "create_at": comment.create_at,
                "author_id": comment.author_id,
                "post_id": comment.post_id,
                "is_published": comment.is_published
            }

            return CommentSchema.model_validate(obj=comment_dict)