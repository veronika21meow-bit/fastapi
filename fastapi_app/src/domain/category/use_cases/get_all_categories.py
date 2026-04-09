from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import Category as Category
from typing import List


class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> List[Category]:
        with self._database.session() as session:
            with self._database.session() as session:
                categories = self._repo.get_all_categories(session)
                result = []
                for category in categories:
                    result.append(Category.model_validate(obj=category))
                return result