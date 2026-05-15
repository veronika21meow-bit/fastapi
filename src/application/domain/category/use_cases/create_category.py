from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.categories import CategoryRepository
from application.schemas.categories import Category, BaseCategory as CreateCategory
from application.core.exceptions.database_exceptions import CategorySlugAlreadyExistsException
from application.core.exceptions.domain_exceptions import CategorySlugIsNotUniqueException

class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_data:CreateCategory) -> Category:
        async with self._database.session() as session:
            try:
                category = await self._repo.create_category(session=session, category_data=category_data)
            except CategorySlugAlreadyExistsException:
                error = CategorySlugIsNotUniqueException(slug=category_data.slug)
                raise error

            return Category.model_validate(obj=category)