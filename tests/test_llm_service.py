
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from task_01_api.llm_service import generate_reply


@pytest.mark.asyncio
async def test_generate_reply_returns_fake_response():
    fake_response = SimpleNamespace(
        text="Dependency injection supplies required objects.",
        model_version="fake-model",
        usage_metadata=SimpleNamespace(
            prompt_token_count=10,
            candidates_token_count=12,
        ),
    )

    with patch(
        "task_01_api.llm_service.client.aio.models.generate_content",
        new_callable=AsyncMock,
        return_value=fake_response,
    ) as mock_generate:
        result = await generate_reply("Explain dependency injection.")

    assert result.answer == "Dependency injection supplies required objects."
    assert result.model == "fake-model"
    assert result.input_tokens == 10
    assert result.output_tokens == 12

    mock_generate.assert_awaited_once()
