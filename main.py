"""Main file"""

from fastapi import FastAPI

from app.middlewares import RecordRequestMiddleware
from app.routers import mock_login, request, credentials, mock_users, mock_points

app = FastAPI()

app.add_middleware(RecordRequestMiddleware, excluded_prefixes=["/api/system/"])

app.include_router(router=mock_login.router, tags=["Login"], prefix="/api/v2/login")
app.include_router(router=mock_users.router, tags=["Users"], prefix="/api/v2/users")
app.include_router(router=mock_points.router, tags=["Points"], prefix="/api/v2/points")

app.include_router(
    router=request.router, tags=["Request"], prefix="/api/system/requests"
)
app.include_router(
    router=credentials.router, tags=["Credentials"], prefix="/api/system/credentials"
)
