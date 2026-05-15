from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.categories import CategoryRepository
from application.core.exceptions.database_exceptions import CategoryNotFoundException
from application.core.exceptions.domain_exceptions import CategoryNotFoundByIdException


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        async with self._database.session() as session:
            try:
                self._repo.delete_category(session=session, category_id=category_id)
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=category_id)
                raise error