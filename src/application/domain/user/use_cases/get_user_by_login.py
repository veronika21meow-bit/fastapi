import logging

from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from application.schemas.users import User
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository

logger = logging.getLogger(__name__)


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str, current_user: User) -> User:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_user_by_login(session, login)
            except UserNotFoundException:
                error = UserNotFoundByLoginException(login=login)
                logger.error(error.get_detail())
                logger.error(
                    f"Пользователь {current_user.login} довел приложение до ошибки: {error.get_detail()}"
                )
                raise error
            return User.model_validate(obj=user)
