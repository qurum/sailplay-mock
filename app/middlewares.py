import http
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.database import ApiRequest
from app.schemas.api_request import ApiRequestBaseSchema


class RecordRequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_prefixes=None):
        super().__init__(app)
        if excluded_prefixes is None:
            excluded_prefixes = []
        self.excluded_prefixes = excluded_prefixes

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # Не сохранять перенаправления
        if response.status_code == http.HTTPStatus.TEMPORARY_REDIRECT:
            return response

        # Не сохранять обращения к исключенным префиксам
        route = request.url.path
        for excluded_prefix in self.excluded_prefixes:
            if route.startswith(excluded_prefix):
                return response

        api_request = ApiRequestBaseSchema(
            method=request.method,
            route=request.url.path,
            headers=request.headers,
            body=await request.body(),
            host=request.client.host,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        ApiRequest.insert_one(api_request.model_dump())

        return response
