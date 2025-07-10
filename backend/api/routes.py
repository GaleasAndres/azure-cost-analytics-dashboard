from fastapi import APIRouter
from . import router as api_router

api = APIRouter()
api.include_router(api_router)
