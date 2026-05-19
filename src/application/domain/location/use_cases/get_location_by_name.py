import logging

from application.core.exceptions.database_exceptions import LocationNotFoundException
from application.core.exceptions.domain_exceptions import (
    LocationNotFoundByNameException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)
from application.schemas.locations import Location

logger = logging.getLogger(__name__)


class GetLocationByNameUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, name: str) -> Location:
        async with self._database.session() as session:
            try:
                location = await self._repo.get_location_by_name(session, name)
            except LocationNotFoundException:
                error = LocationNotFoundByNameException(name=name)
                logger.error(error.get_detail())
                raise error
            return Location.model_validate(obj=location)
