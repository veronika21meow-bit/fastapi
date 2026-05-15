from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.locations import LocationRepository
from application.schemas.locations import Location
from application.core.exceptions.database_exceptions import LocationNotFoundException
from application.core.exceptions.domain_exceptions import LocationNotFoundByIdException

class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> Location:
        async with self._database.session() as session:
            try:
                location = await self._repo.get_location_by_id(session, location_id)
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=location_id)
                raise error
            return Location.model_validate(obj=location)