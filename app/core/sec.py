from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Optional, cast

import jwt
from argon2 import PasswordHasher
from argon2 import exceptions as argon2_exceptions
from fastapi import Depends
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.oauth2 import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request

from app.core import exc, log, settings
from app.core.db.postgres import async_session


class CustomOAuth2PasswordBearer(OAuth2):
    """Custom OAuth2 Password Bearer that looks for access token in
    headers or cookies, and in that order. If not found, it will raise
    an HTTPException with status code 401"""

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict[str, str]] = None,
        description: Optional[str] = None,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password=cast(Any, {'tokenUrl': tokenUrl, 'scopes': scopes})
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=False,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        # Try to get access token from headers
        authorization = request.headers.get('Authorization')
        scheme, token = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != 'bearer':
            # If not found in headers, try in the Authorization header
            token = request.cookies.get('access_token')
            if not token:
                # If no token found, raise an exception
                raise exc.UnauthorizedException('Not authenticated')
        return token


auth2_scheme = CustomOAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')


ALGORITHM = settings.security.algorithm
SECRET = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.security.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.security.refresh_token_expire_minutes

PWD_CONTEXT = PasswordHasher()


class SecurityService:
    @staticmethod
    def create_access_token(data_to_encode: dict) -> str:
        """Creates an access token with the data

        Args:
            data_to_encode (dict): data to encode in jwt token

        Raises:
            exc.InternalServerErrorException: Error creating access jwt token

        Returns:
            str: the encoded token
        """
        try:
            expires = datetime.now(timezone.utc) + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
            data_to_encode.update({'exp': expires, 'type': 'access'})
            encoded_jwt = SecurityService._create_token(data_to_encode)
            return encoded_jwt
        except Exception:
            log.error('Error creating access jwt token')
            raise exc.InternalServerErrorException()

    @staticmethod
    def create_refresh_token(data_to_encode: dict) -> str:
        """Creates an refresh token with the data

        Args:
            data_to_encode (dict): data to encode in jwt token

        Raises:
            exc.InternalServerErrorException: Error creating refresh jwt token

        Returns:
            str: the encoded token
        """
        try:
            expires = datetime.now(timezone.utc) + timedelta(
                minutes=REFRESH_TOKEN_EXPIRE_MINUTES
            )
            data_to_encode.update({'exp': expires, 'type': 'refresh'})
            encoded_jwt = SecurityService._create_token(data_to_encode)
            return encoded_jwt
        except Exception:
            log.error('Error creating refresh jwt token')
            raise exc.InternalServerErrorException()

    @staticmethod
    def verify_token(token: str) -> dict:
        """Verifies if the token is valid

        Args:
            token (str): The token to be verified

        Raises:
            exc.UnauthorizedException: if the token is not valid

        Returns:
            dict: The decoded token
        """
        try:
            data = jwt.decode(jwt=token, key=SECRET, algorithms=[ALGORITHM])
            return data
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            raise exc.UnauthorizedException()

    @staticmethod
    def _create_token(to_encode: dict) -> str:
        try:
            encoded = jwt.encode(
                payload=to_encode,
                algorithm=ALGORITHM,
                key=SECRET,
            )
            return encoded
        except Exception:
            log.error('Error encoding jwt token')
            raise

    @staticmethod
    def get_password_hash(plain_password: str) -> str:
        try:
            hashed_password = PWD_CONTEXT.hash(plain_password)
            return hashed_password
        except argon2_exceptions.HashingError:
            log.error('Error hashing password in get_password_hash')
            raise exc.InternalServerErrorException()

    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        try:
            is_valid = PWD_CONTEXT.verify(password=password, hash=hash)
            return is_valid
        except (
            argon2_exceptions.InvalidHashError,
            argon2_exceptions.VerificationError,
            argon2_exceptions.VerifyMismatchError,
        ):
            return False


def get_current_user(token: Annotated[str, Depends(auth2_scheme)]):
    """Dependency that gets the current user from the token or cookie"""

    user = SecurityService.verify_token(token)
    if not user['type'] == 'access':
        raise exc.UnauthorizedException('Invalid token type')
    return user


async def get_db_user(user: Annotated[dict, Depends(get_current_user)]):
    """Dependency that gets the current user from the database"""
    models = __import__('app.models.user', fromlist=['user'])

    async with async_session() as session:
        db_user = await session.get(models.User, user['sub'])
        if not db_user:
            raise exc.UnauthorizedException()

    return db_user


def get_refresh_token(request: Request) -> str:
    """Get the refresh token from the request headers"""
    authorization = request.headers.get('X-Refresh-Token')
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        raise exc.UnauthorizedException('No refresh token provided')
    return token
