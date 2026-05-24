from typing import Type

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserLoginAlreadyExistsException,
    UserNotFoundException,
)
from application.infrastructure.postgres.models.users import User
from application.resources.auth import get_password_hash
from application.schemas.users import CreateUser


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> User:
        query = select(self._model).where(self._model.id == user_id)
        user = await session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    async def get_user_by_login(self, session: AsyncSession, login: str) -> User:
        query = select(self._model).where(self._model.login == login)
        user = await session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    async def get_user_by_email(self, session: AsyncSession, email: str) -> User:
        query = select(self._model).where(self._model.email == email)
        user = await session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    async def delete_user(self, session: AsyncSession, user_id: int) -> None:
        user = await self.get_user_by_id(session, user_id)
        await session.delete(user)

    async def create_user(self, session: AsyncSession, user_data: CreateUser) -> User:
        user_dict = user_data.model_dump()
        user_dict["password"] = get_password_hash(user_dict.pop("password"))
        query = insert(self._model).values(user_dict).returning(self._model)
        try:
            user = await session.scalar(query)
            return user
        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e).lower()
            if "users_login_key" in error_msg:
                raise UserLoginAlreadyExistsException()
            elif "users_email_key" in error_msg:
                raise UserEmailAlreadyExistsException()
            raise

    async def update_user(
        self, session: AsyncSession, user_id: int, user_data: CreateUser
    ) -> User:
        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data.pop("password"))
        query = (
            update(self._model)
            .where(self._model.id == user_id)
            .values(update_data)
            .returning(self._model)
        )
        try:
            user = await session.scalar(query)
            if not user:
                raise UserNotFoundException()
            return user
        except IntegrityError as e:
            await session.rollback()
            error_msg = str(e).lower()
            if "users_login_key" in error_msg:
                raise UserLoginAlreadyExistsException()
            if "users_email_key" in error_msg:
                raise UserEmailAlreadyExistsException()
            raise