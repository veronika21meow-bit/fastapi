from typing import Type

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.users import User


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get_user_by_id(self, session: Session, id: int) -> User:
        query = (
            session.query(self._model)
            .where(self._model.id == id)
        )
        return query.scalar()
    
    def get_user_by_login(self, session: Session, login: str) -> User:
        query = (
            session.query(self._model)
            .where(self._model.login == id)
        )
        return query.scalar()
    
    def get_user_by_email(self, session: Session, email: str) -> User:
        query = (
            session.query(self._model)
            .where(self._model.email == email)
        )
        return query.scalar()
    
    def delete_user(self, session: Session, id: int) -> bool:
        user = self.get_user_by_id(session, id)
        if user:
            session.delete(user)
            session.commit()
            return True
        return False
    
    def create_user(self, session:Session, login: str, email: str,
                    password: str, first_name: str | None = None,
                    last_name: str | None = None) -> User:
        user = User(
            login=login,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        session.add(user)
        session.flush()
        return user
    