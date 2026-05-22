from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

EXCLUDED_PATHS = [
    "/",
    "/docs",
    "/openapi.json",
    "/api/v1/users/register",
    "/api/v1/auth/login",
    "/api/v1/users/login"
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"error": "Missing or invalid authorization header"}
            )
        return await call_next(request)
