import logging
from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import User
from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exceptions import UserNotFoundByEmailException

logger = logging.getLogger(__name__)

class GetUserByEmailUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, email: str, current_user: User) -> User:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_user_by_email(session, email)
            except UserNotFoundException:
                error = UserNotFoundByEmailException(email=email)
                logger.error(error.get_detail())
                logger.error(
                    f"Пользователь {current_user.email} довел приложение до ошибки: {error.get_detail()}"
                )
                raise error
            return User.model_validate(obj=user)