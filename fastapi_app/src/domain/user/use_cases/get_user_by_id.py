from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByIdException


class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> User:
        with self._database.session() as session:
            try:
                user = self._repo.get_user_by_id(session, user_id)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                raise error
            return User.model_validate(obj=user)