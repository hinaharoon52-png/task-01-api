
class LLMUnavailableError(Exception):
    """The LLM provider is unavailable or timed out."""


class LLMRateLimitError(Exception):
    """The LLM provider rate limit has been reached."""


class LLMAuthenticationError(Exception):
    """The LLM provider authentication or configuration failed."""
