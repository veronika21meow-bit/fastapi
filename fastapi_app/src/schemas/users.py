from pydantic import BaseModel, SecretStr, Field, EmailStr, ConfigDict, field_validator
from fastapi import HTTPException, status


# class User(BaseModel):
#     id: int
#     email : EmailStr
#     login: str
#     first_name: str | None = Field(None, max_length=20)
#     last_name: str | None = Field(None, max_length=20)
#     password: SecretStr

class BaseUser(BaseModel):
    email : EmailStr
    login: str
    first_name: str | None = Field(None, max_length=20)
    last_name: str | None = Field(None, max_length=20)


class User(BaseUser):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    password: SecretStr


class CreateUser(BaseUser):
    password: str

    @field_validator("password", mode="after")
    @staticmethod
    def check_password(password: str) -> str:
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Пароль должен быть не менее 8 символов"
            )
        return password




