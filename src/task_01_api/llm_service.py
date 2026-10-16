
from dataclasses import dataclass

from google import genai

from task_01_api.settings import settings


@dataclass
class LLMResult:
    answer: str
    model: str
    input_tokens: int | None
    output_tokens: int | None


client = genai.Client(api_key=settings.gemini_api_key)


async def generate_reply(message: str) -> LLMResult:
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=message,
        config={
            "max_output_tokens": 500,
            "http_options": {
                "timeout": int(settings.llm_timeout_seconds * 1000),
            },
        },
    )

    usage = response.usage_metadata

    return LLMResult(
        answer=response.text or "",
        model=response.model_version or settings.gemini_model,
        input_tokens=usage.prompt_token_count if usage else None,
        output_tokens=usage.candidates_token_count if usage else None,
    )
