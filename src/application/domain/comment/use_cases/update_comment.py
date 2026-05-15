from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.comments import CommentRepository
from application.schemas.comments import Comment

class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, id: int, text: str,
        is_published: bool = True
    ) -> Comment:
        async with self._database.session() as session:

            updated = await self._repo.update_comment(
                session,
                text,
                id,
                is_published
            )
            session.commit()
            if not updated:
                raise ValueError(f"Комментарий с id '{id}' не найден")
            comment_dict = {
                "id": updated.id,
                "text": updated.text,
                "is_published": updated.is_published,
                "author_id": updated.author_id,
                "post_id": updated.post_id,
                "create_at": updated.create_at
            }
            
            return Comment.model_validate(obj=comment_dict)