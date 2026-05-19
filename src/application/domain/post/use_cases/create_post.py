import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    UserNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.posts import BasePost as CreatePost
from application.schemas.posts import Post

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, post_data: CreatePost) -> Post:
        async with self._database.session() as session:
            try:
                post = await self._repo.create_post(
                    session=session, post_data=post_data
                )
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=post_data.author_id)
                logger.error(error.get_detail())
                raise error
            except CategoryNotFoundException:
                if post_data.category_id is not None:
                    error = CategoryNotFoundByIdException(id=post_data.category_id)
                    raise error
                error = CategoryNotFoundException()
                logger.error(error.get_detail())
                raise error
            except LocationNotFoundException:
                if post_data.location_id is not None:
                    error = LocationNotFoundByIdException(id=post_data.location_id)
                    logger.error(error.get_detail())
                    raise error
                error = LocationNotFoundException()
                logger.error(error.get_detail())
                raise error

            return Post.model_validate(obj=post)
