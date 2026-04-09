"""allow_null_post_id_in_comments

Revision ID: 06c5fb9fabd8
Revises: e8c8d21b6427
Create Date: 2026-04-10 01:14:21.319983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06c5fb9fabd8'
down_revision: Union[str, Sequence[str], None] = 'e8c8d21b6427'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Отключаем проверку внешних ключей для SQLite
    op.execute("PRAGMA foreign_keys=OFF")
    
    # Создаём новую таблицу с правильной схемой
    op.execute("""
        CREATE TABLE comments_new (
            id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            text TEXT NOT NULL,
            is_published BOOLEAN NOT NULL DEFAULT 1,
            create_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            post_id INTEGER,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    """)
    
    # Копируем данные
    op.execute("""
        INSERT INTO comments_new (id, text, is_published, create_at, post_id, author_id)
        SELECT id, text, is_published, create_at, post_id, author_id FROM comments
    """)
    
    # Удаляем старую таблицу
    op.execute("DROP TABLE comments")
    
    # Переименовываем новую
    op.execute("ALTER TABLE comments_new RENAME TO comments")
    
    # Включаем проверку внешних ключей обратно
    op.execute("PRAGMA foreign_keys=ON")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("PRAGMA foreign_keys=OFF")
    
    # Создаём таблицу с NOT NULL constraint
    op.execute("""
        CREATE TABLE comments_old (
            id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            text TEXT NOT NULL,
            is_published BOOLEAN NOT NULL DEFAULT 1,
            create_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            post_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    """)
    
    # Копируем данные, заменяя NULL на 0
    op.execute("""
        INSERT INTO comments_old (id, text, is_published, create_at, post_id, author_id)
        SELECT id, text, is_published, create_at, COALESCE(post_id, 0), author_id FROM comments
    """)
    
    op.execute("DROP TABLE comments")
    op.execute("ALTER TABLE comments_old RENAME TO comments")
    
    op.execute("PRAGMA foreign_keys=ON")