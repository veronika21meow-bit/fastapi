from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.posts import PostRepository
from application.core.exceptions.database_exceptions import PostNotFoundException
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException

class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> None:
        async with self._database.session() as session:
            try:
                self._repo.delete_post(session=session, post_id=post_id)
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                raise error