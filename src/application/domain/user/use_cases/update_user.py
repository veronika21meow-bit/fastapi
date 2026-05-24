import logging

from application.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserLoginAlreadyExistsException,
)
from application.core.exceptions.domain_exceptions import (
    UserEmailIsNotUniqueException,
    UserLoginIsNotUniqueException,
)
from application.schemas.users import CreateUser, User
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository

logger = logging.getLogger(__name__)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, user_data: CreateUser) -> User:
        async with self._database.session() as session:
            try:
                user = await self._repo.update_user(
                    session=session, user_id=user_id, user_data=user_data
                )
                await session.commit()
                await session.refresh(user)
            except UserLoginAlreadyExistsException:
                error = UserLoginIsNotUniqueException(login=user_data.login)
                logger.error(error.get_detail())
                raise error
            except UserEmailAlreadyExistsException:
                error = UserEmailIsNotUniqueException(email=user_data.email)
                logger.error(error.get_detail())
                raise error
            return User.model_validate(obj=user)
