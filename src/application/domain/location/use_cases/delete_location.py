from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.locations import LocationRepository
from application.core.exceptions.database_exceptions import LocationNotFoundException
from application.core.exceptions.domain_exceptions import LocationNotFoundByIdException

class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        async with self._database.session() as session:
            try:
                self._repo.delete_location(session=session, location_id=location_id)
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=location_id)
                raise error