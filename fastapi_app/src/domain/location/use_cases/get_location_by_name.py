from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import Location as LocationSchema


class GetLocationByNameUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, name: int) -> LocationSchema:
        with self._database.session() as session:
            location = self._repo.get_location_by_name(session, name)
            if not location:
                raise ValueError(f"Локация с именем '{name}' не найдена")
            location_dict = {
                "id": location.id,
                "name": location.name,
                "is_published": location.is_published,
                "create_at": location.create_at
            }

            return LocationSchema.model_validate(obj=location_dict)