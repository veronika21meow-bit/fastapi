from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from infrastructure.sqlite.repositories.users import UserRepository
from infrastructure.sqlite.repositories.posts import PostRepository

from schemas.comments import Comment as CommentSchema


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UserRepository()
        self._post_repo = PostRepository()


    async def execute(self, text: str, author_id: int,
                      post_id: int, is_published: bool = True) -> CommentSchema:
        with self._database.session() as session:
            user = self._user_repo.get_user_by_id(session, author_id)
            post = self._post_repo.get_post_by_id(session, post_id)
            if not user and not post:
                raise ValueError(f"Пользователь с id '{author_id}' и пост с id '{post_id}' не найден")
            if not user:
                raise ValueError(f"Пользователь с id '{author_id}' не найден")
            if not post:
                raise ValueError(f"Пост с id '{post_id}' не найден")
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