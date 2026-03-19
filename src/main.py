"""
ThutoQuest-AI FastAPI Entry Point
Main application server for the Grade 10 student mastery tracker
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events"""
    # Startup
    logger.info("Starting ThutoQuest-AI application")
    yield
    # Shutdown
    logger.info("Shutting down ThutoQuest-AI application")


# Initialize FastAPI application
app = FastAPI(
    title="ThutoQuest-AI",
    description="Grade 10 Student Mastery Tracker API",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "ThutoQuest-AI",
            "version": "0.1.0"
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to ThutoQuest-AI",
        "documentation": "/docs",
        "openapi_schema": "/openapi.json"
    }


# TODO: Add route imports
# from src.interfaces.routes import students, curriculum, mastery, assessments
# app.include_router(students.router)
# app.include_router(curriculum.router)
# app.include_router(mastery.router)
# app.include_router(assessments.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
