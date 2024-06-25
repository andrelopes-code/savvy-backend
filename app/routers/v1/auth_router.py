from fastapi import APIRouter

from app.core import exc
from app.core.dependencies import (
    AsyncDBSessionDepends,
    LoginFormDataDepends,
    RefreshTokenDepends,
)
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
        to_encode_data = {'sub': user.id}
        access_token = SecurityService.create_access_token(to_encode_data)
        refresh_token = SecurityService.create_refresh_token(to_encode_data)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
        }

    raise exc.UnauthorizedException()


@router.post('/token/refresh')
async def refresh_token(
    refresh_token: RefreshTokenDepends,
    session: AsyncDBSessionDepends,
):
    # Verify the refresh token
    decoded_token = SecurityService.verify_token(refresh_token)
    if not decoded_token['type'] == 'refresh':
        raise exc.UnauthorizedException('Invalid token type')

    # Get the user from the database and check if it exists
    user_id = decoded_token['sub']
    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(user_id)
    if not user:
        raise exc.UnauthorizedException('Invalid user')

    # Create new access and refresh tokens
    to_encode_data = {'sub': user.id}
    new_access_token = SecurityService.create_access_token(to_encode_data)
    new_refresh_token = SecurityService.create_refresh_token(to_encode_data)

    return {
        'access_token': new_access_token,
        'refresh_token': new_refresh_token,
        'token_type': 'Bearer',
    }
