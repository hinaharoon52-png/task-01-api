
from unittest.mock import AsyncMock, patch

import pytest

from app.services.llm import GeminiLLMService


@pytest.mark.asyncio
async def test_generate_reply_returns_fake_response():
    fake_response = type(
        "FakeResponse",
        (),
        {
            "text": "This is a fake response.",
            "model_version": "fake-model",
            "usage_metadata": type(
                "FakeUsage",
                (),
                {
                    "prompt_token_count": 5,
                    "candidates_token_count": 7,
                },
            )(),
        },
    )()

    with patch(
        "app.services.llm.get_settings"
    ) as mock_settings:
        mock_settings.return_value.gemini_model = "fake-model"
        mock_settings.return_value.max_output_tokens = 500
        mock_settings.return_value.gemini_api_key = "fake-test-key"
        mock_settings.return_value.llm_timeout_seconds = 30

        service = GeminiLLMService()

    service.client.aio.models.generate_content = AsyncMock(
        return_value=fake_response
    )

    result = await service.generate_reply("Hello")

    assert result.answer == "This is a fake response."
    assert result.model == "fake-model"
    assert result.input_tokens == 5
    assert result.output_tokens == 7

    service.client.close()
