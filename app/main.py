from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import router
from app.core.config import settings
from app.core.logging import logger
from app.schemas.response import ErrorDetail, ResponseError  # Import the schemas


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App init")
    yield
    logger.info("App stopped")


limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(
    title="Task Manager - Backend - FastAPI",
    description="REST API for an task manager api",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.include_router(router.api_router, prefix="/api")

# --- Exception Handlers ---


# Handler for FastAPI's HTTPException (and Starlette's underlying HTTPException)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(exc.detail)
    error_detail = ErrorDetail(
        code=f"HTTP_{exc.status_code}", message=exc.detail, field=None
    )
    response_error = ResponseError(success=False, errors=[error_detail])
    return JSONResponse(status_code=exc.status_code, content=response_error.dict())


# Handler for Pydantic validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors_list = []

    for error in exc.errors():
        # error["loc"] es una tupla como ("body", "password") o ("query", "page")
        loc = error["loc"]

        # Si empieza con "body", quitamos ese primer elemento
        if loc and loc[0] == "body":
            field = ".".join(map(str, loc[1:])) if len(loc) > 1 else None
        else:
            field = ".".join(map(str, loc))

        logger.error(f"VALIDATION ERROR - {field} - {error['msg']}")
        errors_list.append(
            ErrorDetail(code="VALIDATION_ERROR", message=error["msg"], field=field)
        )

    response_error = ResponseError(success=False, errors=errors_list)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response_error.dict()
    )


# Generic handler for any other unhandled exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    error_detail = ErrorDetail(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected server error occurred.",
        field=None,
    )
    logger.error(error_detail)
    response_error = ResponseError(success=False, errors=[error_detail])
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response_error.dict()
    )
