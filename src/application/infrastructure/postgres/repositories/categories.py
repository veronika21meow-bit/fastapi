from typing import List, Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException,
    CategoryTitleAlreadyExistsException,
)
from application.infrastructure.postgres.models.categories import Category
from application.schemas.categories import BaseCategory as CreateCategory


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    async def get_category_by_id(self, session: AsyncSession, id: int) -> Category:
        query = select(self._model).where(self._model.id == id)
        category = await session.scalar(query)
        if not category:
            raise CategoryNotFoundException()
        return category

    async def get_category_by_title(
        self, session: AsyncSession, title: str
    ) -> Category:
        query = select(self._model).where(self._model.title == title)
        category = await session.scalar(query)
        if not category:
            raise CategoryNotFoundException()
        return category

    async def get_category_by_slug(self, session: AsyncSession, slug: str) -> Category:
        query = select(self._model).where(self._model.slug == slug)
        category = await session.scalar(query)
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
        await session.delete(category)

    async def create_category(
        self, session: AsyncSession, category_data: CreateCategory
    ) -> Category:
        category_dict = category_data.model_dump(exclude_none=True)
        query = insert(self._model).values(category_dict).returning(self._model)

        try:
            category = await session.scalar(query)
            return category
        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e).lower()

            if "categories_slug_key" in error_msg:
                raise CategorySlugAlreadyExistsException()
            elif "categories_title_key" in error_msg:
                raise CategoryTitleAlreadyExistsException()
            raise
