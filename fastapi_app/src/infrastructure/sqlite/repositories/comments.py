from typing import Type, List
from datetime import datetime

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.comments import Comment


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get_comment_by_id(self, session: Session, id: int) -> Comment:
        query = (
            session.query(self._model)
            .where(self._model.id == id)
        )
        return query.scalar()
    
    def get_all_comments(self, session: Session) -> List[Comment]:
        query = session.query(self._model).all()
        return query

    def delete_comment(self, session: Session, id: int) -> bool:
        comment = self.get_comment_by_id(session, id)
        if comment:
            session.delete(comment)
            session.commit()
            return True
        return False
    
    def create_comment(self, session:Session, text: str,
                       author_id: int, post_id: int,
                       is_published: bool = True) -> Comment:
        comment = Comment(
            text=text,
            is_published=is_published,
            author_id=author_id,
            post_id=post_id,
            create_at=datetime.now(),
        )
        session.add(comment)
        session.commit()
        return comment
    
    def update_comment(self, session:Session, text: str, id: int,
                       is_published: bool = True) -> Comment:
        comment = self.get_comment_by_id(session, id)
        if comment:
            comment.text = text
            comment.is_published = is_published
            session.commit()
        return comment
