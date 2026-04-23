from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User, CreateUser
from core.exceptions.database_exceptions import (
    UserLoginAlreadyExistsException,
    UserEmailAlreadyExistsException
)
from core.exceptions.domain_exceptions import (
    UserLoginIsNotUniqueException,
    UserEmailIsNotUniqueException
)
import logging

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: CreateUser) -> User:
        with self._database.session() as session:
            try:
                user = self._repo.create_user(session=session, user_data=user_data)
            except UserLoginAlreadyExistsException:
                error = UserLoginIsNotUniqueException(
                    login=user_data.login
                )
                logger.error(error.get_detail())
                raise error
            except UserEmailAlreadyExistsException:
                error = UserEmailIsNotUniqueException(
                    email=user_data.email
                )
                logger.error(error.get_detail())
                raise error
            return User.model_validate(obj=user)
        
