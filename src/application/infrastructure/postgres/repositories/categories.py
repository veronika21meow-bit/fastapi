from typing import Type, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.schemas.categories import BaseCategory as CreateCategory
from application.infrastructure.postgres.models.categories import Category
from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException,
    CategoryTitleAlreadyExistsException
)


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    async def get_category_by_id(self, session: AsyncSession, id: int) -> Category:
        query = select(self._model).where(self._model.id == id)
        result = await session.execute(query)
        category = result.scalar_one_or_none()

        if not category:
            raise CategoryNotFoundException()

        return category
    
    async def get_category_by_title(self, session: AsyncSession, title: str) -> Category:
        query = select(self._model).where(self._model.title == title)
        result = await session.execute(query)
        category = result.scalar_one_or_none()

        if not category:
            raise CategoryNotFoundException()

        return category
    
    async def get_category_by_slug(self, session: AsyncSession, slug: str) -> Category:
        query = select(self._model).where(self._model.slug == slug)
        result = await session.execute(query)
        category = result.scalar_one_or_none()

        if not category:
            raise CategoryNotFoundException()

        return category
    
    async def get_all_categories(self, session: AsyncSession) -> List[Category]:
        query = select(self._model).order_by(self._model.title)
        result = await session.execute(query)
        categories = result.scalars().all()

        return categories
    
    async def delete_category(self, session: AsyncSession, category_id: int) -> None:
        category = await self.get_category_by_id(session, category_id)

        if category:
            await session.delete(category)
            await session.flush()
        else:
            raise CategoryNotFoundException()
    
    async def create_category(self, session:AsyncSession, category_data:CreateCategory) -> Category:
        existing_by_slug = await session.execute(
            select(self._model).where(self._model.slug == category_data.slug)
        )
        if existing_by_slug.scalar_one_or_none():
            raise CategorySlugAlreadyExistsException()
        existing_by_title = await session.execute(
            select(self._model).where(self._model.title == category_data.title)
        )
        if existing_by_title.scalar_one_or_none():
            raise CategoryTitleAlreadyExistsException()
        data = category_data.model_dump(exclude_none=True)        
        category = self._model(**data)
        session.add(category)
        await session.flush()
        await session.refresh(category)
        return category
