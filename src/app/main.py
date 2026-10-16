
from uuid import uuid4
import re

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import router as v1_router
from app.core.exceptions import (
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMUnavailableError,
)
from app.schemas.chat import ErrorResponse, ErrorDetail


app = FastAPI(title="Task 04 - Maintainable Chat API", version="0.4.0")

REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,100}$")


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    supplied_id = request.headers.get("X-Request-ID", "")

    if REQUEST_ID_PATTERN.fullmatch(supplied_id):
        request_id = supplied_id
    else:
        request_id = str(uuid4())

    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


def error_response(
    request: Request,
    status_code: int,
    code: str,
    message: str,
) -> JSONResponse:
    body = ErrorResponse(
        error=ErrorDetail(
            code=code,
            message=message,
            request_id=getattr(request.state, "request_id", str(uuid4())),
        )
    )
    return JSONResponse(
        status_code=status_code,
        content=body.model_dump(),
    )


@app.exception_handler(LLMUnavailableError)
async def llm_unavailable_handler(request: Request, exc: LLMUnavailableError):
    return error_response(
        request, 503, "llm_unavailable",
        "The chatbot service is temporarily unavailable.",
    )


@app.exception_handler(LLMRateLimitError)
async def llm_rate_limit_handler(request: Request, exc: LLMRateLimitError):
    return error_response(
        request, 429, "llm_rate_limited",
        "The chatbot service is receiving too many requests. Try again later.",
    )


@app.exception_handler(LLMAuthenticationError)
async def llm_authentication_handler(
    request: Request, exc: LLMAuthenticationError
):
    return error_response(
        request, 502, "llm_configuration_error",
        "The chatbot service could not complete the request.",
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request, exc: RequestValidationError
):
    return error_response(
        request, 422, "invalid_request",
        "The request is invalid. Check the submitted fields.",
    )


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    return error_response(
        request, exc.status_code, "http_error", "The request could not be completed."
    )


app.include_router(v1_router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": app.version}


@app.get("/")
async def root():
    return {"message": "Chat API is running"}
