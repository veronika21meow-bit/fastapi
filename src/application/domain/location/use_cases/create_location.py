import logging

from application.core.exceptions.database_exceptions import (
    LocationNameAlreadyExistsException,
)
from application.core.exceptions.domain_exceptions import (
    LocationNameIsNotUniqueException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)
from application.schemas.locations import BaseLocation as CreateLocation
from application.schemas.locations import Location

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: CreateLocation) -> Location:
        async with self._database.session() as session:
            try:
                location = await self._repo.create_location(
                    session=session, location_data=location_data
                )
            except LocationNameAlreadyExistsException:
                error = LocationNameIsNotUniqueException(name=location_data.name)
                logger.error(error.get_detail())
                raise error

            return Location.model_validate(obj=location)
