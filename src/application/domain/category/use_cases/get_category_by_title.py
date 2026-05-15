from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.categories import CategoryRepository
from application.schemas.categories import Category
from application.core.exceptions.database_exceptions import CategoryNotFoundException
from application.core.exceptions.domain_exceptions import CategoryNotFoundByTitleException


class GetCategoryByTitleUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, title: str) -> Category:
        async with self._database.session() as session:
            try:
                category = await self._repo.get_category_by_title(session, title)
            except CategoryNotFoundException:
                error = CategoryNotFoundByTitleException(title=title)
                raise error
            return Category.model_validate(obj=category)