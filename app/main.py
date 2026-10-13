from fastapi import FastAPI

from app.api.resources import router as resources_router

app = FastAPI(
    title="Cloud Resource Janitor",
    description=(
        "Read-only AWS and Azure resource inventory and "
        "cleanup recommendation platform."
    ),
    version="0.1.0",
)

app.include_router(resources_router)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "name": "Cloud Resource Janitor",
        "status": "running",
        "documentation": "/docs",
    }


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "cloud-resource-janitor",
    }