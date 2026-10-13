# Task 01 API

A simple REST API built with FastAPI and Uvicorn.

## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/)

## Project Setup

Clone the repository and navigate to the project directory.

Install dependencies:

```bash
uv sync
```

## Run the API

Start the development server:

```bash
uv run uvicorn api.main:app --app-dir src --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

## Health Check

Send a GET request to:

`http://127.0.0.1:8000/health`

Expected response:

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

## Environment Variables

See `.env.example` for example environment variables.

## Technology Stack

- Python
- FastAPI
- Uvicorn
- uv
