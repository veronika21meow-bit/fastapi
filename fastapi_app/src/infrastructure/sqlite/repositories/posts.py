from typing import Type, List
from datetime import datetime

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.posts import Post


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get_post_by_id(self, session: Session, id: int) -> Post:
        query = (
            session.query(self._model)
            .where(self._model.id == id)
        )
        return query.scalar()
    
    def get_post_by_author(self, session: Session, author_id: int) -> Post:
        query = (
            session.query(self._model)
            .where(self._model.author_id == author_id)
        )
        return query.scalar()
    
    def get_all_posts(self, session: Session) -> List[Post]:
        query = session.query(self._model).all()
        return query

    
    def delete_post(self, session: Session, id: int) -> bool:
        post = self.get_post_by_id(session, id)
        if post:
            session.delete(post)
            session.commit()
            return True
        return False
    
    def create_post(self, session:Session, title: str, text: str,
                    author_id: int, location_id: int | None = None,
                    category_id: int | None = None, image: str | None = None,
                    pub_date: datetime | None = None, is_published: bool = True) -> Post:
        post = Post(
            title=title,
            text=text,
            is_published=is_published,
            author_id=author_id,
            location_id=location_id,
            category_id=category_id,
            image=image,
            pup_date=pub_date,
            create_at=datetime.now(),
        )
        session.add(post)
        session.commit()
        return post
    
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
