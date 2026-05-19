import logging

from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserPermissionDeniedException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import User

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, current_user: User) -> None:
        if current_user.id != user_id:
            error = UserPermissionDeniedException()
            logger.error(error.get_detail())
            logger.error(
                f"Пользователь {current_user.login} попытался удалить пользователя с id={user_id}"
            )
            raise error
        async with self._database.session() as session:
            try:
                await self._repo.delete_user(session=session, user_id=user_id)
                await session.commit()
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error
