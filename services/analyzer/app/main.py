"""NeuroHunter Analyzer Service main module."""

from contextlib import asynccontextmanager

from app.api.routes.vacancies import router as vacancies_router
from app.database.mongodb import create_mongo_client
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongo = create_mongo_client()

    try:
        await app.state.mongo.admin.command({'ping': 1})

        print("MongoDB connection established.")

        yield

    finally:
        await app.state.mongo.close()

        print("MongoDB connection closed.")


app = FastAPI(
    title="NeuroHunter Analyzer Service",
    description="NeuroHunter Analyzer Service",
    version="0.0.1",
    lifespan=lifespan,
)


@app.get('/health', tags=["Health"])
async def health():
    """Get health status of the service."""
    return {"status": "ok"}

app.include_router(vacancies_router)
