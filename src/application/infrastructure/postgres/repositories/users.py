from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from application.infrastructure.postgres.models.users import User
from application.schemas.users import CreateUser
from application.core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserEmailAlreadyExistsException,
    UserLoginAlreadyExistsException
)
from application.resources.auth import get_password_hash


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> User:
        query = select(self._model).where(self._model.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundException()
        return user
    
    async def get_user_by_login(self, session: AsyncSession, login: str) -> User:
        query = select(self._model).where(self._model.login == login)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundException()
        return user
    
    async def get_user_by_email(self, session: AsyncSession, email: str) -> User:
        query = select(self._model).where(self._model.email == email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundException()
        return user
    
    async def delete_user(self, session: AsyncSession, user_id: int) -> None:
        user = await self.get_user_by_id(session, user_id)
        await session.delete(user)
    
    async def create_user(self, session: AsyncSession, user_data: CreateUser) -> User:
        query = select(self._model).where(
            or_(
                self._model.login == user_data.login,
                self._model.email == user_data.email,
            )
        )
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            if existing_user.login == user_data.login:
                raise UserLoginAlreadyExistsException()
            elif existing_user.email == user_data.email:
                raise UserEmailAlreadyExistsException()
        
        user_dict = user_data.model_dump()
        user_dict['password'] = get_password_hash(user_dict.pop('password'))
        
        new_user = self._model(**user_dict)
        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)
        
        return new_user