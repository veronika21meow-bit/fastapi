from typing import Type, List
from datetime import datetime

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.locations import Location


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get_location_by_id(self, session: Session, id: int) -> Location:
        query = (
            session.query(self._model)
            .where(self._model.id == id)
        )
        return query.scalar()
    
    def get_location_by_name(self, session: Session, name: str) -> Location:
        query = (
            session.query(self._model)
            .where(self._model.name == name)
        )
        return query.scalar()
    
    def get_all_locations(self, session: Session) -> List[Location]:
        query = session.query(self._model).all()
        return query

    
    def delete_location(self, session: Session, id: int) -> bool:
        location = self.get_location_by_id(session, id)
        if location:
            session.delete(location)
            session.commit()
            return True
        return False
    
    def create_location(self, session:Session, name: str,
                        is_published: bool = True) -> Location:
        location = Location(
            name=name,
            is_published=is_published,
            create_at=datetime.now()
        )
        session.add(location)
        session.commit()
        return location
    
    def update_location(self, session:Session, id: int, 
                        name: str) -> Location:
        location = self.get_location_by_id(session, id)
        if location:
            location.name=name
            session.commit()
        return location
