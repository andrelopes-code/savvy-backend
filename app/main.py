from fastapi import FastAPI

from app.routers.v1 import main_router

APP_NAME = 'Savvy API'
VERSION = '0.1.0'

# Initialize the FastAPI app
app = FastAPI(title=APP_NAME, version=VERSION)

# Include the main router to the main app
app.include_router(main_router)
