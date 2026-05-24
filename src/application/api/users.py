from fastapi import APIRouter, Depends, HTTPException, status

from application.api.depends import (
    create_user_use_case,
    delete_user_use_case,
    get_user_by_email_use_case,
    get_user_by_id_use_case,
    get_user_by_login_use_case,
    update_user_use_case,
)
from application.core.exceptions.domain_exceptions import (
    UserEmailIsNotUniqueException,
    UserLoginIsNotUniqueException,
    UserNotFoundByEmailException,
    UserNotFoundByIdException,
    UserNotFoundByLoginException,
    UserPermissionDeniedException,
)
from application.domain.user.use_cases.create_user import CreateUserUseCase
from application.schemas.users import CreateUser, User
from application.services.auth import AuthService

users_router = APIRouter()


@users_router.get(
    "/profile/{user_id}", status_code=status.HTTP_200_OK, response_model=User
)
async def get_user_by_id(
    user_id: int,
    user: User = Depends(AuthService.get_current_user),
    use_case=Depends(get_user_by_id_use_case),
) -> User:
    try:
        return await use_case.execute(user_id=user_id, current_user=user)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@users_router.get("/login/{login}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user_by_login(
    login: str,
    user: User = Depends(AuthService.get_current_user),
    use_case=Depends(get_user_by_login_use_case),
) -> User:
    try:
        return await use_case.execute(login=login, current_user=user)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@users_router.get("/email/{email}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user_by_email(
    email: str,
    user: User = Depends(AuthService.get_current_user),
    use_case=Depends(get_user_by_email_use_case),
) -> User:
    try:
        return await use_case.execute(email=email, current_user=user)
    except UserNotFoundByEmailException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@users_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=User
)
async def create_user(
    user_data: CreateUser, use_case: CreateUserUseCase = Depends(create_user_use_case)
) -> User:
    try:
        return await use_case.execute(user_data=user_data)
    except (
        UserLoginIsNotUniqueException,
        UserEmailIsNotUniqueException,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user: User = Depends(AuthService.get_current_user),
    use_case=Depends(delete_user_use_case),
) -> None:
    try:
        await use_case.execute(user_id=user_id, current_user=user)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except UserPermissionDeniedException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )


@users_router.post(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
    dependencies=[Depends(AuthService.get_current_user)],
)
async def update_user(
    user_id: int,
    user_data: CreateUser,
    use_case: CreateUserUseCase = Depends(update_user_use_case),
) -> User:
    try:
        return await use_case.execute(user_id=user_id, user_data=user_data)
    except (UserLoginIsNotUniqueException, UserEmailIsNotUniqueException) as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
