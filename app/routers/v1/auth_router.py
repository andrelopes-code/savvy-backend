from fastapi import APIRouter

from app.core import exc
from app.core.dependencies import AsyncDBSessionDepends, LoginFormDataDepends
from app.core.sec import SecurityService
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix='/auth')


@router.post('/token')
async def login_user(
    form_data: LoginFormDataDepends, session: AsyncDBSessionDepends
):
    user_repository = UserRepository(session)
    email = form_data.username
    password = form_data.password

    user = await user_repository.get_by_email(email)

    # Check if user exists, if exists, check if password is correct
    # if password is correct, create an access token and return it
    if user and SecurityService.verify_password(password, user.password):
        data = {'sub': user.id}
        return {
            'access_token': SecurityService.create_access_token(data),
            'refresh_token': SecurityService.create_refresh_token(data),
            'token_type': 'Bearer',
        }

    raise exc.UnauthorizedException()
