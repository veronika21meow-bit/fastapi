from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import Category
from core.exceptions.database_exceptions import CategoryNotFoundException
from core.exceptions.domain_exceptions import CategoryNotFoundByTitleException


class GetCategoryByTitleUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, title: str) -> Category:
        with self._database.session() as session:
            try:
                category = self._repo.get_category_by_title(session, title)
            except CategoryNotFoundException:
                error = CategoryNotFoundByTitleException(title=title)
                raise error
            return Category.model_validate(obj=category)