from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import Post as PostSchema


class GetPostsByAuthorUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, author_id: int) -> List[PostSchema]:
        with self._database.session() as session:
            posts = self._repo.get_posts_by_author(session, author_id)
            return [PostSchema.model_validate(post) for post in posts]