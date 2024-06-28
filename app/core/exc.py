from fastapi import FastAPI, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.core.log import log


def configure_exception_handlers(app: FastAPI):
    """Configure exception handlers

    Args:
        app (FastAPI): The FastAPI app
    """

    @app.exception_handler(SQLAlchemyError)
    async def db_exception_handler(_, exc):
        log.error(f'Database error occurred: {type(exc)}')
        raise HTTPException(status_code=500, detail='Internal server error')


"""
Custom HTTP Exceptions for the APP
"""


class NotFoundException(HTTPException):
    def __init__(self, detail: str = 'Resource not found'):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = 'Unauthorized'):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'},
        )


class BadRequestException(HTTPException):
    def __init__(self, detail: str = 'Bad request'):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


class InternalServerErrorException(HTTPException):
    def __init__(self, detail: str = 'Internal server error'):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = 'Forbidden'):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
