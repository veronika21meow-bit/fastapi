from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> bool:
        with self._database.session() as session:
            success = self._repo.delete_user(session, user_id)
            return success