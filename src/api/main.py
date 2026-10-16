
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from google.genai import errors

from task_01_api.llm_service import generate_reply


app = FastAPI(
    title="Task 03 - LLM Chat API",
    version="0.3.0",
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message cannot be empty or whitespace.")
        return value


class Usage(BaseModel):
    input_tokens: int | None = None
    output_tokens: int | None = None


class ChatResponse(BaseModel):
    answer: str
    model: str
    usage: Usage


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": app.version}


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await generate_reply(request.message)

        return ChatResponse(
            answer=result.answer,
            model=result.model,
            usage=Usage(
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
            ),
        )

    except errors.APIError as exc:
        print(f"Gemini API error: {exc!r}")
        status_code = getattr(exc, "code", None)

        if status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="LLM provider rate limit reached. Try again later.",
            ) from None

        if status_code in (401, 403):
            raise HTTPException(
                status_code=502,
                detail="LLM provider authentication failed.",
            ) from None

        if status_code in (408, 504):
            raise HTTPException(
                status_code=504,
                detail="LLM provider request timed out.",
            ) from None

        raise HTTPException(
            status_code=502,
            detail="LLM provider returned an error.",
        ) from None

    except TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="LLM provider request timed out.",
        ) from None

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="LLM provider is temporarily unavailable.",
        ) from None
        
       