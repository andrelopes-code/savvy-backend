from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.core.log import log


def configure_exception_handlers(app: FastAPI):
    """Configure exception handlers

    Args:
        app (FastAPI): The FastAPI app
    """

    @app.exception_handler(SQLAlchemyError)
    async def db_exception_handler(_, exc):
        log.error(f'Database error occurred: {exc} : {type(exc)}')
        return HTTPException(status_code=500, detail='Internal server error')
