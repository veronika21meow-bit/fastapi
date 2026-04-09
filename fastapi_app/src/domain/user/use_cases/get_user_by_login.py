from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByLoginException
from schemas.users import User


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> User:
        with self._database.session() as session:
            try:
                user = self._repo.get_user_by_login(session, login)
            except UserNotFoundException:
                error = UserNotFoundByLoginException(login=login)
                raise error
            return User.model_validate(obj=user)