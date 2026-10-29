from fastapi import FastAPI

from app.api.findings import router as findings_router
from app.api.resources import router as resources_router
from app.api.scan import router as scan_router
from app.api.summary import router as summary_router


app = FastAPI(
    title="Cloud Resource Janitor",
    description=(
        "Read-only AWS and Azure resource inventory and "
        "cleanup recommendation platform."
    ),
    version="0.1.0",
)

app.include_router(resources_router)
app.include_router(findings_router)
app.include_router(summary_router)
app.include_router(scan_router)


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