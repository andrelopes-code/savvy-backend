from fastapi import APIRouter

from .auth_router import router as auth_router
from .record_router import router as record_router
from .user_router import router as user_router

# The main router that will be used by the app for all v1 routes
main_router = APIRouter(prefix='/api/v1')

# Include sub-routers
main_router.include_router(auth_router, tags=['Auth'])
main_router.include_router(user_router, tags=['User'])
main_router.include_router(record_router, tags=['Record'])
