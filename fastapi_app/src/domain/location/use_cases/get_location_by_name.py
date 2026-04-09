from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import Location
from core.exceptions.database_exceptions import LocationNotFoundException
from core.exceptions.domain_exceptions import LocationNotFoundByNameException

class GetLocationByNameUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, name: int) -> Location:
        with self._database.session() as session:
            try:
                location = self._repo.get_location_by_id(session, name)
            except LocationNotFoundException:
                error = LocationNotFoundByNameException(name=name)
                raise error
            return Location.model_validate(obj=location)