from src.application.infrastructure.postgres.database import database
from src.application.infrastructure.postgres.repositories.locations import LocationRepository
from application.schemas.locations import Location
from application.core.exceptions.database_exceptions import LocationNotFoundException
from application.core.exceptions.domain_exceptions import LocationNotFoundByNameException

class GetLocationByNameUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, name: int) -> Location:
        async with self._database.session() as session:
            try:
                location = await self._repo.get_location_by_id(session, name)
            except LocationNotFoundException:
                error = LocationNotFoundByNameException(name=name)
                raise error
            return Location.model_validate(obj=location)
