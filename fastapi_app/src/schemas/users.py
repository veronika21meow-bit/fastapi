from pydantic import BaseModel, SecretStr, Field, EmailStr


class User(BaseModel):
    id: int
    email : EmailStr
    login: str
    first_name: str | None = Field(None, max_length=20)
    last_name: str | None = Field(None, max_length=20)
    password: SecretStr
