import logging

from application.core.exceptions.database_exceptions import LocationNotFoundException
from application.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)
from application.schemas.locations import Location

logger = logging.getLogger(__name__)


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
                logger.error(error.get_detail())
                raise error
            return Location.model_validate(obj=location)
