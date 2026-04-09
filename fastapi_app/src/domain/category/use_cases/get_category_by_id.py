from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import Category
from core.exceptions.database_exceptions import CategoryNotFoundException
from core.exceptions.domain_exceptions import CategoryNotFoundByIdException

class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> Category:
        with self._database.session() as session:
            try:
                category = self._repo.get_category_by_id(session, category_id)
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=category_id)
                raise error
            return Category.model_validate(obj=category)