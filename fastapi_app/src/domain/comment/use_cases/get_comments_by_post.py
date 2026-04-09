from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import Comment


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> List[Comment]:
        with self._database.session() as session:
            comments = self._repo.get_all_comments(session)

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