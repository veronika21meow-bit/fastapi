from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import insert, select, or_
from infrastructure.sqlite.models.users import User
from schemas.users import CreateUser
from core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserEmailAlreadyExistsException,
    UserLoginAlreadyExistsException
)

from resources.auth import get_password_hash


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get_user_by_id(self, session: Session, user_id: int) -> User:
        query = (
            session.query(self._model)
            .where(self._model.id == user_id)
        )
        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user
    
    def get_user_by_login(self, session: Session, login: str) -> User:
        query = (
            session.query(self._model)
            .where(self._model.login == login)
        )
        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user
    
    def get_user_by_email(self, session: Session, email: str) -> User:
        query = (
            session.query(self._model)
            .where(self._model.email == email)
        )
        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user
    
    def delete_user(self, session: Session, user_id: int) -> None:
        user = self.get_user_by_id(session, user_id)
        if user:
            session.delete(user)
        else:
            raise UserNotFoundException()
    
    def create_user(self, session: Session, user_data: CreateUser) -> User:
        existing_user = session.scalar(
            select(self._model).where(
                or_(self._model.login == user_data.login,
                    self._model.email == user_data.email,
                )
            )
        )
        if existing_user is not None:
            if existing_user.login == user_data.login:
                raise UserLoginAlreadyExistsException()
            elif existing_user.email == user_data.email:
                raise UserEmailAlreadyExistsException()
        
        user = user_data.model_dump()
        user['password'] = get_password_hash(user['password'])
        
        query = (
            insert(self._model)
            .values(user) 
            .returning(self._model)
        )
        return session.scalar(query)
    