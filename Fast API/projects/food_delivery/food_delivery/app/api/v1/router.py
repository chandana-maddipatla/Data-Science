from fastapi import APIRouter
from app.api.v1.routes import user, opportunity, workflow, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(opportunity.router, prefix="/opportunities", tags=["Opportunities"])
api_router.include_router(workflow.router, prefix="/workflows", tags=["Workflows"])
