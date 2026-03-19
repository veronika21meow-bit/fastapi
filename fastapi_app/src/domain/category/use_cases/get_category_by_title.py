from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import Category as CategorySchema


class GetCategoryByTitleUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, title: str) -> CategorySchema:
        with self._database.session() as session:
            category = self._repo.get_category_by_title(session, title)
            if not category:
                raise ValueError(f"Категория с title '{title}' не найдена")
            category_dict = {
                "id": category.id,
                "title": category.title,
                "description": category.description,
                "slug": category.slug,
                "is_published": category.is_published,
                "create_at": category.create_at
            }
            return CategorySchema.model_validate(obj=category_dict)