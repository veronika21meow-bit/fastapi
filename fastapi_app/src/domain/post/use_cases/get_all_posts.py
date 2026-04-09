from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import Post


class GetAllPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self) -> List[Post]:
        with self._database.session() as session:
            posts = self._repo.get_all_posts(session)
            result = []
            for post in posts:
                result.append(Post.model_validate(obj=post))
            return result