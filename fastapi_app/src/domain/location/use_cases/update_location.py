from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import Location as LocationSchema

class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, id: int, name: str) -> LocationSchema:
        with self._database.session() as session:
            updated = self._repo.update_location(session, id, name)
            session.commit()
            if not updated:
                raise ValueError(f"Локация с id '{id}' не найдена")
           
            location_data = {
                "id":updated.id,
                "name":updated.name,
                "is_published":updated.is_published,
                "create_at":updated.create_at
            }

            return LocationSchema.model_validate(obj=location_data)