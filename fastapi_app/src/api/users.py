from fastapi import APIRouter, status, HTTPException, Depends
from schemas.users import User

from api.depends import (
    get_user_by_id_use_case,
    get_user_by_login_use_case,
    get_user_by_email_use_case,
    create_user_use_case,
    delete_user_use_case,
)

users_router = APIRouter()


@users_router.get("/profile/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user_by_id(
    user_id: int,
    use_case = Depends(get_user_by_id_use_case)) -> User:
    try:
        user = await use_case.execute(user_id=user_id)
        return user
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@users_router.get("/login/{login}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user_by_login(
    login: str,
    use_case = Depends(get_user_by_login_use_case)) -> User:
    try:
        user = await use_case.execute(login=login)
        return user
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    
@users_router.get("/email/{email}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user_by_email(
    email: str,
    use_case = Depends(get_user_by_email_use_case)) -> User:
    try:
        user = await use_case.execute(email=email)
        return user
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@users_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)  
async def create_user(
    login: str,
    email: str,
    password: str,
    first_name: str | None = None,
    last_name: str | None = None,
    use_case = Depends(create_user_use_case)) -> User:
    try:
        user = await use_case.execute(
            login=login,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    use_case = Depends(delete_user_use_case)) -> None: 
    try:
        result = await use_case.execute(user_id=user_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )