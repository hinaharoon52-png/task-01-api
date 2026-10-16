
import logging
from dataclasses import dataclass
from typing import Protocol

from google import genai
from google.genai import errors

from app.core.config import get_settings
from app.core.exceptions import (
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMUnavailableError,
)

logger = logging.getLogger(__name__)


@dataclass
class LLMResult:
    answer: str
    model: str
    input_tokens: int | None
    output_tokens: int | None


class LLMService(Protocol):
    async def generate_reply(self, message: str) -> LLMResult:
        ...


class GeminiLLMService:
    def __init__(self) -> None:
        settings = get_settings()

        self.model = settings.gemini_model
        self.max_output_tokens = settings.max_output_tokens
        self.timeout_ms = int(settings.llm_timeout_seconds * 1000)

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    async def generate_reply(self, message: str) -> LLMResult:
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=message,
                config={
                    "max_output_tokens": self.max_output_tokens,
                    "http_options": {
                        "timeout": self.timeout_ms,
                    },
                },
            )

        except errors.APIError as exc:
            status_code = getattr(exc, "code", None)

            # Temporary diagnostics: do not log credentials or request data.
            logger.error(
                "Gemini API error: type=%s, status=%s",
                type(exc).__name__,
                status_code,
            )

            if status_code == 429:
                raise LLMRateLimitError() from None

            if status_code in (401, 403):
                raise LLMAuthenticationError() from None

            raise LLMUnavailableError() from None

        except Exception as exc:
            # Temporary diagnostics; avoid printing exception text because
            # it may contain sensitive request or configuration information.
            logger.error(
                "Gemini request failed: type=%s",
                type(exc).__name__,
            )
            raise LLMUnavailableError() from None

        usage = response.usage_metadata

        return LLMResult(
            answer=response.text or "",
            model=response.model_version or self.model,
            input_tokens=(
                usage.prompt_token_count
                if usage is not None
                else None
            ),
            output_tokens=(
                usage.candidates_token_count
                if usage is not None
                else None
            ),
        )
