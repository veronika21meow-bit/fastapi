from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import Post
from core.exceptions.database_exceptions import PostNotFoundException
from core.exceptions.domain_exceptions import PostNotFoundByIdException


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> Post:
        with self._database.session() as session:
            with self._database.session() as session:
                try:
                    post = self._repo.get_post_by_id(session, post_id)
                except PostNotFoundException:
                    error = PostNotFoundByIdException(id=post_id)
                    raise error

                return Post.model_validate(obj=post)