from fastapi import APIRouter, status, HTTPException
from schemas.posts import Post
from schemas.users import User


router = APIRouter()


@router.get("/hello_world", status_code=status.HTTP_200_OK)
async def get_hello_world() -> dict:
    response = {"text": "Hello, World!"}
    return response


@router.post("/test_json", status_code=status.HTTP_201_CREATED, response_model=Post)
async def test_json(post: Post) -> dict:
    if len(post.text) < 3:
        raise HTTPException(
            detail="Длина поста должна быть не меньше 3 символов",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    response = {
        "post_text": post.text,
        "author_name": post.author.login
    }

    return Post.model_validate(obj=response)


@router.post("/register_user/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def register_user(user: User) -> dict:
    if len(user.password < 8):
        raise HTTPException(
            detail="Длина пароля должна быть не меньше 8 символов",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )
    response = {"message": "User registered successfully", "user": user}
    return response


@router.delete("/delete_user/", status_code=status.HTTP_200_OK)
async def delete_user(user: User) -> dict:
    response = {"message": "User deleted successfully", "user": user}
    return response


@router.put("/update_post/", status_code=status.HTTP_200_OK)
async def delete_user(post: Post) -> dict:
    response = {"message": "Post update successfully", "post": post}
    return response


@router.get("/meow", status_code=status.HTTP_200_OK)
async def get_hello_world() -> dict:
    response = {"text": "MEOW!"}
    return response


