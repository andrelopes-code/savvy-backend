from argon2 import PasswordHasher

from app.core import settings

ALGORITHM = settings.security.algorithm
SECRET = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.security.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.security.refresh_token_expire_minutes

PWD_CONTEXT = PasswordHasher()


class SecurityService:
    @staticmethod
    def _create_token(to_encode: dict) -> str: ...

    @staticmethod
    def create_access_token(data_to_encode: dict) -> str: ...

    @staticmethod
    def create_refresh_token(data_to_encode: dict) -> str: ...

    @staticmethod
    def verify_token(token: str) -> dict: ...

    @staticmethod
    def get_password_hash(plain_password: str) -> str:
        hashed_password = PWD_CONTEXT.hash(plain_password)
        return hashed_password

    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        is_valid = PWD_CONTEXT.verify(password=password, hash=hash)
        return is_valid
