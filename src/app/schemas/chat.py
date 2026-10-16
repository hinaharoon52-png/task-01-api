
from pydantic import BaseModel, Field, field_validator

from app.core.config import get_settings


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty or whitespace.")

        max_length = get_settings().max_input_length
        if len(value) > max_length:
            raise ValueError(
                f"Message must not exceed {max_length} characters."
            )

        return value


class Usage(BaseModel):
    input_tokens: int | None = None
    output_tokens: int | None = None


class ChatResponse(BaseModel):
    answer: str
    model: str
    usage: Usage


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
