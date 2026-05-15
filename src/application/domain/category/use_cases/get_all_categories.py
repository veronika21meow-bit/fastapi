from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.categories import CategoryRepository
from application.schemas.categories import Category as Category
from typing import List


class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> List[Category]:
        async with self._database.session() as session:
            categories = await self._repo.get_all_categories(session)
            result = []
            for category in categories:
                result.append(Category.model_validate(obj=category))
            return result