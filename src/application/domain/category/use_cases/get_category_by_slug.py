from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.categories import CategoryRepository
from application.schemas.categories import Category
from application.core.exceptions.database_exceptions import CategoryNotFoundException
from application.core.exceptions.domain_exceptions import CategoryNotFoundBySlugException

class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> Category:
        async with self._database.session() as session:
            try:
                category = await self._repo.get_category_by_slug(session, slug)
            except CategoryNotFoundException:
                error = CategoryNotFoundBySlugException(slug=slug)
                raise error
            return Category.model_validate(obj=category)