from typing import Type, List
from datetime import datetime

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.categories import Category


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get_category_by_id(self, session: Session, id: int) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.id == id)
        )
        return query.scalar()
    
    def get_category_by_title(self, session: Session, title: str) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.title == title)
        )
        return query.scalar()
    
    def get_category_by_slug(self, session: Session, slug: str) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.slug == slug)
        )
        return query.scalar()
    
    def get_all_categories(self, session: Session) -> List[Category]:
        query = session.query(self._model).all()
        return query
    
    def delete_category(self, session: Session, id: int) -> bool:
        category = self.get_category_by_id(session, id)
        if category:
            session.delete(category)
            session.commit()
            return True
        return False
    
    def create_category(self, session:Session, title: str, description: str,
                        slug: str, is_published: bool = True) -> Category:
        category = Category(
            title=title,
            description=description,
            slug=slug,
            is_published=is_published,
            create_at=datetime.now(),
        )
        session.add(category)
        session.commit()
        return category
    
    def update_category(self, session:Session, id: int, title: str, description: str,
                        slug: str, is_published: bool = True) -> Category:
        category = self.get_category_by_id(session, id)
        if category:
            category.title=title
            category.description=description
            category.slug = slug
            category.is_published = is_published
            session.commit()
        return category
