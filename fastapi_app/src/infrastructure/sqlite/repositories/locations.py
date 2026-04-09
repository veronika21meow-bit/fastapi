from typing import Type, List
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from infrastructure.sqlite.models.locations import Location
from schemas.locations import BaseLocation as CreateLocation
from core.exceptions.database_exceptions import (
    LocationNotFoundException,
    LocationNameAlreadyExistsException
)

class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get_location_by_id(self, session: Session, id: int) -> Location:
        query = (
            session.query(self._model)
            .where(self._model.id == id)
        )
        location = query.scalar()
        if not location:
            raise LocationNotFoundException()
        return location
    
    def get_location_by_name(self, session: Session, name: str) -> Location:
        query = (
            session.query(self._model)
            .where(self._model.name == name)
        )
        location = query.scalar()
        if not location:
            raise LocationNotFoundException()
        return location
    
    def get_all_locations(self, session: Session) -> List[Location]:
        query = session.query(self._model).all()
        return query
    
    def delete_location(self, session: Session, location_id: int) -> None:
        location = self.get_location_by_id(session, location_id)
        if location:
            session.delete(location)
        else:
            raise LocationNotFoundException()
    
    def create_location(self, session:Session, location_data: CreateLocation) -> Location:
        existing_location = session.scalar(
            select(self._model).where(self._model.name == location_data.name)
        )
        if existing_location is not None:
            raise LocationNameAlreadyExistsException()
        query = (
            insert(self._model)
            .values(location_data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        return session.scalar(query)
    

