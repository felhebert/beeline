"""Beeline - Main API file. """
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette_prometheus import metrics, PrometheusMiddleware

from beeline.api.routers import api_router

application = FastAPI()
application.add_middleware(PrometheusMiddleware)
application.add_route("/metrics", metrics)

application.include_router(api_router)


@application.get("/")
async def home():
    """ Redirect to docs. """
    return RedirectResponse(url="/redoc")


@application.get("/heartbeat")
async def heartbeat() -> None:
    """ Health probing endpoint. """
    pass
