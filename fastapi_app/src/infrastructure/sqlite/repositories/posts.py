from typing import Type, List

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from infrastructure.sqlite.models.posts import Post
from infrastructure.sqlite.models.users import User
from infrastructure.sqlite.models.locations import Location
from infrastructure.sqlite.models.categories import Category
from schemas.posts import BasePost as CreatePost, UpdatePost
from core.exceptions.database_exceptions import (
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException 
)


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post
        self._author_model: Type[User] = User
        self._location_model: Type[Location] = Location
        self._category_model: Type[Category] = Category
    def get_post_by_id(self, session: Session, id: int) -> Post | None:
        query = (
            session.query(self._model)
            .where(self._model.id == id)
        )
        post = query.scalar()
        if not post:
            raise PostNotFoundException()
        return post
    
    def get_posts_by_author(self, session: Session, author_id: int) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.author_id == author_id)
        )
        posts = query.all()
        if not posts:
            raise PostNotFoundException()
        return posts
    
    def get_all_posts(self, session: Session) -> List[Post]:
        query = session.query(self._model).all()
        return query

    
    def delete_post(self, session: Session, post_id: int) -> None:
        post = self.get_post_by_id(session, post_id)
        if post:
            session.delete(post)
        else:
            raise PostNotFoundException()
    
    def create_post(self, session:Session, post_data: CreatePost) -> Post:
        author = session.get(self._author_model, post_data.author_id)
        if not author:
            raise UserNotFoundException()
        if post_data.location_id is not None:
            location = session.get(self._location_model, post_data.location_id)
            if not location:
                raise LocationNotFoundException()
        if post_data.category_id is not None:
            category = session.get(self._category_model, post_data.category_id)
            if not category:
                raise CategoryNotFoundException()
        query = (
            insert(self._model)
            .values(post_data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        return session.scalar(query)
    
    def update_post(self, session:Session, id: int, title: str, 
                    text: str, is_published: bool = True, category_id: int | None = None,
                    image: str | None = None) -> Post:
        post = self.get_post_by_id(session, id)
        if post:
            post.title=title
            post.text = text
            post.is_published = is_published
            post.category_id = category_id
            post.image = image
            session.commit()
        return post
