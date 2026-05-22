from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.database import engine
from app.models.base import Base
from app.models import user, opportunity, workflow

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Delivery API",
    description="A REST API for food delivery platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Resource not found", "path": str(request.url)}
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation failed", "details": exc.errors()}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "message": str(exc)}
    )


app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Food Delivery API is running"}
