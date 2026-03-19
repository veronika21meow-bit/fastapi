from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import Category as CategorySchema


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, title: str, description: str,
                    slug: str, is_published: bool = True) -> CategorySchema:
        with self._database.session() as session:
            existing_title = self._repo.get_category_by_title(session, title)
            existing_slug = self._repo.get_category_by_slug(session, slug)
            if existing_title and existing_slug:
                raise ValueError(f"Пользователь с названием '{title}' и с slug '{slug}' уже существует") 
            if existing_title:
                raise ValueError(f"Пользователь с название '{title}' уже существует")
            if existing_slug:
                raise ValueError(f"Пользователь с slug '{slug}' уже существует") 
            category = self._repo.create_category(
                session=session,
                title=title,
                description=description,
                slug=slug,
                is_published=is_published
            )

            category_data = {
                "id":category.id,
                "title":category.title,
                "description":category.description,
                "slug":category.slug,
                "is_published":category.is_published,
                "create_at":category.create_at
            }

            return CategorySchema.model_validate(obj=category_data)