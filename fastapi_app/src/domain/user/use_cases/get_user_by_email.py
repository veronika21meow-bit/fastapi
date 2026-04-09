from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByEmailException


class GetUserByEmailUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, email: str) -> User:
        with self._database.session() as session:
            try:
                user = self._repo.get_user_by_email(session, email)
            except UserNotFoundException:
                error = UserNotFoundByEmailException(email=email)
                raise error
            return User.model_validate(obj=user)