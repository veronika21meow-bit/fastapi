from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import Post as PostSchema

class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, id: int, title: str, text: str,
        is_published: bool = True,
        category_id: int | None = None,
        image: str | None = None,
    ) -> PostSchema:
        with self._database.session() as session:
            updated = self._repo.update_post(
                session=session,
                id=id,
                title=title,
                text=text,
                is_published=is_published,
                category_id=category_id,
                image=image
            )
            session.commit()
            if not updated:
                raise ValueError(f"Пост с id '{id}' не найден")
            post_dict = {
                "id": updated.id,
                "title": updated.title,
                "text": updated.text,
                "pub_date": updated.pub_date,
                "author_id": updated.author_id,
                "location_id": updated.location_id,
                "category_id": updated.category_id,
                "image": updated.image,
                "create_at": updated.create_at,
                "is_published": updated.is_published
            }
            
            return PostSchema.model_validate(obj=post_dict)