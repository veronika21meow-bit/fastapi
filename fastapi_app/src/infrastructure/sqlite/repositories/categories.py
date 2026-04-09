from typing import Type, List
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from schemas.categories import BaseCategory as CreateCategory
from infrastructure.sqlite.models.categories import Category
from core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException
)


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get_category_by_id(self, session: Session, id: int) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.id == id)
        )
        category = query.scalar()
        if not category:
            raise CategoryNotFoundException()
        return category
    
    def get_category_by_title(self, session: Session, title: str) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.title == title)
        )
        category = query.scalar()
        if not category:
            raise CategoryNotFoundException()
        return category
    
    def get_category_by_slug(self, session: Session, slug: str) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.slug == slug)
        )
        category = query.scalar()
        if not category:
            raise CategoryNotFoundException()
        return category
    
    def get_all_categories(self, session: Session) -> List[Category]:
        query = session.query(self._model).all()
        return query
    
    def delete_category(self, session: Session, category_id: int) -> None:
        category = self.get_category_by_id(session, category_id)
        if category:
            session.delete(category)
        else:
            raise CategoryNotFoundException()
    
    def create_category(self, session:Session, category_data:CreateCategory) -> Category:
        existing_category = session.scalar(
            select(self._model).where(self._model.slug == category_data.slug)
        )
        if existing_category is not None:
            raise CategorySlugAlreadyExistsException()
        query = (
            insert(self._model)
            .values(category_data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        return session.scalar(query)
    

