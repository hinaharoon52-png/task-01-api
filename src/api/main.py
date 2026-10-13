from fastapi import FastAPI

app = FastAPI(
    title="Task 01 API",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": app.version,
    }
