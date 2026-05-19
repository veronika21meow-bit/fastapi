from typing import List, Type

from sqlalchemy import select
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
        result = await session.execute(query)
        location = result.scalar_one_or_none()

        if not location:
            raise LocationNotFoundException()

        return location

    async def get_location_by_name(self, session: AsyncSession, name: str) -> Location:
        query = select(self._model).where(self._model.name == name)
        result = await session.execute(query)
        location = result.scalar_one_or_none()

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
        if location:
            await session.delete(location)
            await session.flush()
        else:
            raise LocationNotFoundException()

    async def create_location(
        self, session: AsyncSession, location_data: CreateLocation
    ) -> Location:
        existing_query = select(self._model).where(
            self._model.name == location_data.name
        )
        existing_result = await session.execute(existing_query)
        existing_location = existing_result.scalar_one_or_none()

        if existing_location is not None:
            raise LocationNameAlreadyExistsException()

        data = location_data.model_dump(exclude_none=True)
        location = self._model(**data)
        session.add(location)
        await session.flush()
        await session.refresh(location)

        return location
