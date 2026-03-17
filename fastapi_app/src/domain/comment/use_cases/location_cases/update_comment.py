from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import Comment as CommentSchema

class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, id: int, text: str,
        is_published: bool = True
    ) -> CommentSchema:
        with self._database.session() as session:

            updated = self._repo.update_comment(
                session,
                text,
                id,
                is_published
            )
            session.commit()
            
            comment_dict = {
                "id": updated.id,
                "text": updated.text,
                "is_published": updated.is_published,
                "author_id": updated.author_id,
                "post_id": updated.post_id,
                "create_at": updated.create_at
            }
            
            return CommentSchema.model_validate(obj=comment_dict)