"""Main router."""
from fastapi import APIRouter

import beeline.api.routes.no_context as no_context

api_router = APIRouter()

# Routers
api_router.include_router(
    no_context.router,
    prefix="/model/no_context",
    tags=["No Context"],
)