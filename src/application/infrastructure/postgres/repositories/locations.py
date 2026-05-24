from typing import List, Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    LocationNameAlreadyExistsException,
    LocationNotFoundException,
)
from application.infrastructure.postgres.models.locations import Location
from application.schemas.locations import BaseLocation as CreateLocation


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    async def get_location_by_id(self, session: AsyncSession, id: int) -> Location:
        query = select(self._model).where(self._model.id == id)
        location = await session.scalar(query)
        if not location:
            raise LocationNotFoundException()
        return location

    async def get_location_by_name(self, session: AsyncSession, name: str) -> Location:
        query = select(self._model).where(self._model.name == name)
        location = await session.scalar(query)
        if not location:
            raise LocationNotFoundException()
        return location

    async def get_all_locations(self, session: AsyncSession) -> List[Location]:
        query = select(self._model)
        result = await session.execute(query)
        locations = result.scalars().all()
        return locations

    async def delete_location(self, session: AsyncSession, location_id: int) -> None:
        location = await self.get_location_by_id(session, location_id)
        await session.delete(location)

    async def create_location(
        self, session: AsyncSession, location_data: CreateLocation
    ) -> Location:
        location_dict = location_data.model_dump(exclude_none=True)
        query = insert(self._model).values(location_dict).returning(self._model)
        try:
            location = await session.scalar(query)
            return location
        except IntegrityError:
            raise LocationNameAlreadyExistsException()
