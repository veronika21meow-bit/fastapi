from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema

class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str, email: str,
                    password: str, first_name: str | None = None,
                    last_name: str | None = None) -> UserSchema:
        with self._database.session() as session:
            user = self._repo.create_user(
                session=session,
                login=login,
                email=email,
                password=password,
                first_name=first_name,                    
                last_name=last_name
            )
            user_data = {
                "id":user.id,
                "login":user.login,
                "email":user.email,
                "password":user.password,
                "first_name":user.first_name,
                "last_name":user.last_name
            }
            return UserSchema.model_validate(obj=user_data)
