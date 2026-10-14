
from fastapi import FastAPI

from api.routes import router


app = FastAPI(
    title="Messages API",
    description="A simple in-memory API for managing messages.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "version": app.version,
    }



