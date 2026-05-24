from uuid import uuid4
import shutil
from pathlib import Path
from fastapi import UploadFile
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository
from application.schemas.posts import PostImageResponse
from application.core.exceptions.domain_exceptions import (
    UploadFileIsNotImageException,
    PostNotFoundByIdException,
)
import logging

logger = logging.getLogger(__name__)


class AddPostImageUseCase:
    def __init__(self) -> None:
        self.image_folder = Path("/fastapi_app/images")
        self._repo = PostRepository()

    async def execute(self, post_id: int, image: UploadFile) -> PostImageResponse:
        async with database.session() as session:
            try:
                post = await self._repo.get_post_by_id(session, post_id)
            except Exception:
                raise PostNotFoundByIdException(id=post_id)
            if not image.filename:
                raise UploadFileIsNotImageException()
            
            file_extension = image.filename.split(".")[-1].lower()
            if file_extension not in ["jpeg", "jpg", "png", "gif"]:
                raise UploadFileIsNotImageException()
            
            self.image_folder.mkdir(parents=True, exist_ok=True)
            new_image_name = str(uuid4())
            new_image_filename = f"{new_image_name}.{file_extension}"
            new_image_path = self.image_folder / new_image_filename
            
            with open(new_image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            await self._repo.add_post_images(
                session=session,
                post_id=post_id,
                image_paths=[new_image_filename]  
            )
            await session.commit()
            logger.info(f"Image added to post {post_id}: {new_image_filename}")
            return PostImageResponse(post_id=post_id, image=new_image_filename)
