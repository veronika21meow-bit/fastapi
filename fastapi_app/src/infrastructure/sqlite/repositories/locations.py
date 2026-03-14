from typing import Type, List
from datetime import datetime

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.locations import Location


class PostRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get_location_by_id(self, session: Session, id: int) -> Location:
        query = (
            session.query(self._model)
            .where(self._model.id == id)
        )
        return query.scalar()
    
    def get_all_locations(self, session: Session) -> List[Location]:
        query = session.query(self._model).all()
        return query

    
    def delete_location(self, session: Session, id: int) -> bool:
        post = self.get_location_by_id(session, id)
        if post:
            session.delete(post)
            session.commit()
            return True
        return False
    
    def create_location(self, session:Session, name: str,
                        is_published: bool = True) -> Location:
        post = Location(
            name=name,
            is_published=is_published,
            create_at=datetime.now()
        )
        session.add(post)
        session.commit()
        return post
    
    def update_location(self, session:Session, id: int, 
                        name: str) -> Location:
        post = self.get_location_by_id(session, id)
        if post:
            post.name=name
            session.commit()
        return post
