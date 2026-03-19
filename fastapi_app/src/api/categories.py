from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.categories import Category

from api.depends import (
    get_all_categories_use_case,
    get_category_by_id_use_case,
    create_category_use_case,
    delete_category_use_case,
    update_category_use_case ,
    get_category_by_slug_use_case,
    get_category_by_title_use_case
)

categories_router = APIRouter()


@categories_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Category])
async def get_all_categories(
    use_case = Depends(get_all_categories_use_case)
) -> List[Category]:
    categories = await use_case.execute()
    return categories


@categories_router.get("/id/{category_id}", status_code=status.HTTP_200_OK, response_model=Category)
async def get_category_by_id(
    category_id: int,
    use_case = Depends(get_category_by_id_use_case)
) -> Category:
    try:
        category = await use_case.execute(category_id=category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с id '{category_id}' не найдена"
            )
        return category
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    

@categories_router.get("/slug/{slug}", status_code=status.HTTP_200_OK, response_model=Category)
async def get_category_by_slug(
    slug: str,
    use_case = Depends(get_category_by_slug_use_case)
) -> Category:
    try:
        category = await use_case.execute(slug=slug)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с slug '{slug}' не найдена"
            )
        return category
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    
@categories_router.get("/title/{title}", status_code=status.HTTP_200_OK, response_model=Category)
async def get_category_by_title(
    title: str,
    use_case = Depends(get_category_by_title_use_case)
) -> Category:
    try:
        category = await use_case.execute(title=title)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с названием '{title}' не найдена"
            )
        return category
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


@categories_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(
    title: str, description: str,
    slug: str, is_published: bool = True,
    use_case = Depends(create_category_use_case)
) -> Category:
    try:
        category = await use_case.execute(
            title=title,
            description=description,
            slug=slug,
            is_published=is_published
        )
        return category
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@categories_router.put("/{category_id}", status_code=status.HTTP_200_OK, response_model=Category)
async def update_category(
    category_id: int,
    category_data: Category,
    use_case = Depends(update_category_use_case)
) -> Category:
    try:
        category = await use_case.execute(
            id=category_id,
            title=category_data.title,
            description=category_data.description,
            slug=category_data.slug,
            is_published=category_data.is_published
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с id '{category_id}' не найдена"
            )
        return category
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    use_case = Depends(delete_category_use_case)
) -> None:
    try:
        result = await use_case.execute(category_id=category_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с id '{category_id}' не найдена"
            )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )