
from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.api.dependencies import get_llm_service
from app.schemas.chat import ChatRequest, ChatResponse, Usage
from app.services.llm import LLMService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse, status_code=200)
async def chat(
    request: ChatRequest,
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
    request_id: Annotated[
        str | None,
        Header(alias="X-Request-ID"),
    ] = None,
) -> ChatResponse:
    result = await llm_service.generate_reply(request.message)

    return ChatResponse(
        answer=result.answer,
        model=result.model,
        usage=Usage(
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
        ),
    )
