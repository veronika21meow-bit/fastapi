from typing import List
from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.comments import CommentRepository
from application.schemas.comments import Comment


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> List[Comment]:
        async with self._database.session() as session:
            comments = await self._repo.get_all_comments(session)

            result = []
            for comment in comments:
                comment_dict = {
                    "id": comment.id,
                    "text": comment.text,
                    "create_at": comment.create_at,
                    "post_id": comment.post_id,
                    "author_id": comment.author_id,
                    "is_published": comment.is_published
                }

                result.append(Comment.model_validate(obj=comment_dict))

            return result