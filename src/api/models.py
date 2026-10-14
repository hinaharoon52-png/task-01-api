
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageCreate(BaseModel):
    role: MessageRole
    content: str = Field(min_length=1, max_length=2000)

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Content cannot be empty or whitespace only.")
        return value


class MessageUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Content cannot be empty or whitespace only.")
        return value


class MessageResponse(BaseModel):
    id: int
    role: MessageRole
    content: str
    created_at: datetime
