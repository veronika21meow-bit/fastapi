from typing import List

from application.schemas.posts import Post
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository


class GetAllPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self) -> List[Post]:
        async with self._database.session() as session:
            posts = await self._repo.get_all_posts(session)
            result = []
            for post in posts:
                result.append(Post.model_validate(obj=post))
            return result
