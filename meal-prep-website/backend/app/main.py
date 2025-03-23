from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .api import api_router
from .database import get_db, create_tables
from .api.recipes import seed_sample_recipes
from .api.users import create_default_user
from .config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

    # Get database session
    db = next(get_db())

    # Seed initial data
    create_default_user(db)
    seed_sample_recipes(db)


# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Meal Prep Assistant API",
        "docs_url": "/docs",
        "api_version": "v1",
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
