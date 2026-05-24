import logging
from typing import List

from application.core.exceptions.domain_exceptions import CommentNotFoundByIdException
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import CommentRepository
from application.schemas.comments import CommentImageResponse

logger = logging.getLogger(__name__)


class GetCommentImagesUseCase:
    def __init__(self) -> None:
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> List[CommentImageResponse]:
        async with database.session() as session:
            try:
                images = await self._repo.get_comment_images(session, comment_id)
            except Exception:
                raise CommentNotFoundByIdException(id=comment_id)

            return [
                CommentImageResponse(comment_id=comment_id, image=img) for img in images
            ]
