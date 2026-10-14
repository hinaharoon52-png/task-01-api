# Task 02 - Messages API

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
## Health Check

The API provides a health-check endpoint at:

http://127.0.0.1:8000/health

A successful response confirms that the API is running.
## Messages API

The API provides endpoints to create, list, retrieve, update, and delete messages.

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/messages` | Create a message |
| GET | `/api/v1/messages` | List messages |
| GET | `/api/v1/messages/{message_id}` | Get a message by ID |
| PATCH | `/api/v1/messages/{message_id}` | Update a message |
| DELETE | `/api/v1/messages/{message_id}` | Delete a message |

### API Documentation

Start the server and open `http://127.0.0.1:8000/docs` to test the endpoints interactively.

Messages are stored in memory and are not preserved when the application restarts.