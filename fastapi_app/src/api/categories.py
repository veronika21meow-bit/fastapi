from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from api.depends import (
    get_all_categories_use_case,
    get_category_by_id_use_case,
    create_category_use_case,
    delete_category_use_case,
    get_category_by_slug_use_case,
    get_category_by_title_use_case
)
from core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategorySlugIsNotUniqueException,
    CategoryNotFoundBySlugException,
    CategoryNotFoundByTitleException,
)
from schemas.categories import Category, BaseCategory as CreateCategory
from services.auth import AuthService

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
        return category
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    

@categories_router.get("/slug/{slug}", status_code=status.HTTP_200_OK, response_model=Category)
async def get_category_by_slug(
    slug: str,
    use_case = Depends(get_category_by_slug_use_case)
) -> Category:
    try:
        category = await use_case.execute(slug=slug)
        return category
    except CategoryNotFoundBySlugException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    
@categories_router.get("/title/{title}", status_code=status.HTTP_200_OK, response_model=Category)
async def get_category_by_title(
    title: str,
    use_case = Depends(get_category_by_title_use_case)
) -> Category:
    try:
        category = await use_case.execute(title=title)
        return category
    except CategoryNotFoundByTitleException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@categories_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category, dependencies=[Depends(AuthService.get_current_user)])
async def create_category(
    category_data: CreateCategory,
    use_case = Depends(create_category_use_case)
) -> Category:
    try:
        return await use_case.execute(category_data=category_data)
    except CategorySlugIsNotUniqueException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    use_case = Depends(delete_category_use_case)
) -> None:
    try:
        await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )