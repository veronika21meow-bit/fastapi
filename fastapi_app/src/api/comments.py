from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.comments import Comment, BaseComment as CreateComment

from api.depends import (
    get_comments_by_post_use_case,
    get_comment_by_id_use_case,
    create_comment_use_case,
    delete_comment_use_case,
    update_comment_use_case,  
)
from core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from services.auth import AuthService

comments_router = APIRouter()


@comments_router.get("/{comment_id}", status_code=status.HTTP_200_OK, response_model=Comment)
async def get_comment_by_id(
    comment_id: int,
    use_case = Depends(get_comment_by_id_use_case)
) -> Comment:
    try:
        comment = await use_case.execute(comment_id=comment_id)
        return comment
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@comments_router.get("/{author_id}", status_code=status.HTTP_200_OK, response_model=Comment)
async def get_comments_by_post(
    author_id: int,
    use_case = Depends(get_comment_by_id_use_case)
) -> Comment:
    try:
        comment = await use_case.execute(author_id=author_id)
        return comment
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

@comments_router.post("/create_comment", status_code=status.HTTP_201_CREATED, response_model=Comment, dependencies=[Depends(AuthService.get_current_user)])
async def create_comment(
    comment_data: CreateComment, 
    use_case = Depends(create_comment_use_case)
) -> Comment:
    try:
        comment = await use_case.execute(comment_data=comment_data)
        return comment
    except (UserNotFoundByIdException, PostNotFoundByIdException) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )


@comments_router.put("/update_comment/{comment_id}", status_code=status.HTTP_200_OK, response_model=Comment, dependencies=[Depends(AuthService.get_current_user)])
async def update_comment(
    comment_id: int,
    text: str,
    is_published: bool = True,
    use_case = Depends(update_comment_use_case)
) -> Comment:
    try:
        comment = await use_case.execute(
            id=comment_id,
            text=text,
            is_published=is_published
        )
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Комментарий с ID {comment_id} не найден"
            )
        return comment
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@comments_router.delete("/delete/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(AuthService.get_current_user)])
async def delete_comment(
    comment_id: int,
    use_case = Depends(delete_comment_use_case)
) -> None:
    try:
        await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )