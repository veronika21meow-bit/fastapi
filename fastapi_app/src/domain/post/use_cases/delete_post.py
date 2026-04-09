from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from core.exceptions.database_exceptions import PostNotFoundException
from core.exceptions.domain_exceptions import PostNotFoundByIdException

class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> None:
        with self._database.session() as session:
            try:
                self._repo.delete_post(session=session, post_id=post_id)
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                raise error