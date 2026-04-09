from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import Location as Location
from typing import List


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> List[Location]:
        with self._database.session() as session:
            locations = self._repo.get_all_locations(session)
            result = []
            for location in locations:
                result.append(Location.model_validate(obj=location))
            return result