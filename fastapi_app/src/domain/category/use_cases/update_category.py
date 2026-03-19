from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import Category as CategorySchema

class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, id: int, title: str,
        description: str, slug: str,
        is_published: bool = True
    ) -> CategorySchema:
        with self._database.session() as session:

            updated = self._repo.update_category(
                session,
                id,
                title,
                description,
                slug,
                is_published
            )
            session.commit()
            if not updated:
                raise ValueError(f"Категория с id '{id}' не найдена")
            category_dict = {
                "id": updated.id,
                "title": updated.title,
                "description": updated.description,
                "slug": updated.slug,
                "is_published": updated.is_published,
                "create_at": updated.create_at
            }
            
            return CategorySchema.model_validate(obj=category_dict)