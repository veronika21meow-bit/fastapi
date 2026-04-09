from datetime import datetime
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.posts import Post, BasePost as CreatePost
from core.exceptions.database_exceptions import (
    UserNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException
)
from core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException
)

class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, post_data: CreatePost) -> Post:
        with self._database.session() as session:
            try:
                post = self._repo.create_post(session=session, post_data=post_data)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=post_data.author_id)
                raise error
            except CategoryNotFoundException:
                if post_data.category_id is not None:
                    error = CategoryNotFoundByIdException(id=post_data.category_id)
                    raise error
                error = CategoryNotFoundException()
                raise error
            except LocationNotFoundException:
                if post_data.location_id is not None:
                    error = LocationNotFoundByIdException(id=post_data.location_id)
                    raise error
                error = LocationNotFoundException()
                raise error

            return Post.model_validate(obj=post)