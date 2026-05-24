import logging
from typing import List

from application.core.exceptions.domain_exceptions import PostNotFoundByIdException
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository
from application.schemas.posts import PostImageResponse

logger = logging.getLogger(__name__)


class GetPostImagesUseCase:
    def __init__(self) -> None:
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> List[PostImageResponse]:
        async with database.session() as session:
            try:
                images = await self._repo.get_post_images(session, post_id)
            except Exception:
                raise PostNotFoundByIdException(id=post_id)

            return [PostImageResponse(post_id=post_id, image=img) for img in images]
