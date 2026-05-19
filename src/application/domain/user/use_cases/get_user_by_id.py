import logging

from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exceptions import UserNotFoundByIdException
from application.schemas.users import User
from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.users import UserRepository

logger = logging.getLogger(__name__)


class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, current_user: User) -> User:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_user_by_id(session, user_id)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                logger.error(
                    f"Пользователь {current_user.login} довел приложение до ошибки: {error.get_detail()}"
                )
                raise error
            return User.model_validate(obj=user)
