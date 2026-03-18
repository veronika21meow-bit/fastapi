from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import Post as PostSchema


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostSchema:
        with self._database.session() as session:
            post = self._repo.get_post_by_id(session, post_id)

            post_dict = {
                "id": post.id,
                "title": post.title,
                "text": post.text,
                "pub_date": post.pub_date,
                "create_at": post.create_at,
                "author_id": post.author_id,
                "location_id": post.location_id,
                "category_id": post.category_id,
                "image": post.image,
                "is_published": post.is_published
            }

            return PostSchema.model_validate(obj=post_dict)