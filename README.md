# Task 04 — Maintainable Chat API

A REST API built with FastAPI and Google Gemini, organized into a maintainable application architecture.

## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Google Gemini API key

## Project Setup

Clone the repository and navigate to the project directory.

Install dependencies:

```bash
uv sync
```

Create a `.env` file in the project root using `.env.example` as a template. Add your Gemini API key to `.env`. Never commit your API key.

## Run the API

```bash
uv run uvicorn app.main:app --app-dir src --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Interactive documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## API Endpoints

### GET `/health`

Example response:

```json
{
  "status": "ok",
  "version": "0.4.0"
}
```

### POST `/api/v1/chat`

Example request:

```json
{
  "message": "What is artificial intelligence?"
}
```

Example successful response:

```json
{
  "answer": "Artificial intelligence enables computers to perform tasks that typically require human intelligence.",
  "model": "gemini-3.7-flash",
  "usage": {
    "input_tokens": 8,
    "output_tokens": 20
  }
}
```

The answer, model name, and token counts depend on the actual provider response.

## Error Handling

Errors use a consistent JSON structure containing an error code, a safe message, and a request ID. The API handles invalid requests, provider unavailability, rate limits, and provider authentication/configuration errors without exposing sensitive provider details.

The `X-Request-ID` response header helps identify and trace each request. A valid supplied request ID is preserved; otherwise, the API generates one.

## Project Architecture

```text
src/app/
├── main.py
├── api/
│   ├── dependencies.py
│   └── v1/
│       ├── router.py
│       └── chat.py
├── core/
│   ├── config.py
│   └── exceptions.py
├── schemas/
│   └── chat.py
└── services/
    └── llm.py
```

- `main.py`: Creates the FastAPI application, middleware, and exception handlers.
- `api/dependencies.py`: Provides the LLM service dependency.
- `api/v1/router.py`: Registers version 1 API routes.
- `api/v1/chat.py`: Implements the chat endpoint.
- `core/config.py`: Loads application settings from environment variables.
- `core/exceptions.py`: Defines provider-related exceptions.
- `schemas/chat.py`: Validates request data and defines response schemas.
- `services/llm.py`: Communicates with Google Gemini and handles provider errors.

## Testing

Run the test suite:

```bash
uv run pytest -v
```

The tests cover health checks, request validation, successful chat responses, request ID handling, safe provider error responses, and the LLM service. Dependency overrides are used to test the API without making real provider calls.

## Environment Variables

See `.env.example` for the required configuration. Keep `.env` private and never commit API keys or other secrets.

## Technology Stack

- Python 3.12
- FastAPI
- Uvicorn
- Google Gemini API
- Pydantic Settings
- uv
- pytest