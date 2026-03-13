from fastapi import APIRouter
from app.api.v1.endpoints import exploration

api_router = APIRouter()
api_router.include_router(exploration.router, tags=["exploration"])
