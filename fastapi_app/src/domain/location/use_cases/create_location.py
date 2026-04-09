from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import Location, BaseLocation as CreateLocation
from core.exceptions.database_exceptions import LocationNameAlreadyExistsException
from core.exceptions.domain_exceptions import LocationNameIsNotUniqueException

class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: CreateLocation) -> Location:
        with self._database.session() as session:
            try:
                location = self._repo.create_location(session=session, location_data=location_data)
            except LocationNameAlreadyExistsException:
                error = LocationNameIsNotUniqueException(name=location_data.name)
                raise error

            return Location.model_validate(obj=location)