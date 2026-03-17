from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import Location as LocationSchema


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationSchema:
        with self._database.session() as session:
            location = self._repo.get_location_by_id(session, location_id)

            location_dict = {
                "id": location.id,
                "name": location.name,
                "is_published": location.is_published,
                "create_at": location.create_at
            }

            return LocationSchema.model_validate(obj=location_dict)