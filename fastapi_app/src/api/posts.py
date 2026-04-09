from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.posts import Post, BasePost as CreatePost

from api.depends import (
    get_all_posts_use_case,
    get_post_by_id_use_case,
    get_posts_by_author_use_case,
    create_post_use_case,
    delete_post_use_case,
    update_post_use_case 
)
from core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    UserNotFoundByIdException
)

posts_router = APIRouter()


@posts_router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=Post)
async def get_post_by_id(
    post_id: int,
    use_case = Depends(get_post_by_id_use_case)
) -> Post:
    try:
        post = await use_case.execute(post_id=post_id)
        return post
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@posts_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Post])
async def get_all_posts(
    use_case = Depends(get_all_posts_use_case)
) -> List[Post]:
    posts = await use_case.execute()
    return posts


@posts_router.get("/author/{author_id}", status_code=status.HTTP_200_OK, response_model=List[Post])
async def get_posts_by_author(
    author_id: int,
    use_case = Depends(get_posts_by_author_use_case)
) -> List[Post]:
    try:
        posts = await use_case.execute(author_id=author_id)
        return posts
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


@posts_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    post_data: CreatePost,
    use_case = Depends(create_post_use_case)) -> Post:
    try:
        return await use_case.execute(post_data=post_data)
    except (
        UserNotFoundByIdException,
        LocationNotFoundByIdException,
        CategoryNotFoundByIdException,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )


@posts_router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=Post)
async def update_post(
    post_id: int,
    post_data: Post,  # Схема для обновления
    use_case = Depends(update_post_use_case)
) -> Post:
    try:
        post = await use_case.execute(
            id=post_id,
            title=post_data.title,
            text=post_data.text,
            is_published=post_data.is_published,
            category_id=post_data.category_id,
            image=post_data.image
        )
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пост с ID {post_id} не найден"
            )
        return post
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@posts_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    use_case = Depends(delete_post_use_case)
) -> None:
    try:
        await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )