from typing import List

from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)
from application.schemas.locations import Location as Location


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> List[Location]:
        async with self._database.session() as session:
            locations = await self._repo.get_all_locations(session)
            result = []
            for location in locations:
                result.append(Location.model_validate(obj=location))
            return result
