"""
FastAPI application entry point.
Configures CORS, middleware, and routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.config.logging import setup_logging
from backend.src.middleware.error_handler import error_handler_middleware
import os


# Setup logging
setup_logging()

# Create FastAPI application
app = FastAPI(
    title="SWAIF Clinic Follow-up System",
    description="Multi-clinic patient follow-up system with gamification and rewards",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8502"],  # Streamlit UIs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handler middleware
app.middleware("http")(error_handler_middleware)

# Include API routers (will be added as routes are implemented)
# from backend.src.api.v1 import auth, clinics, etc.
# app.include_router(auth.router, prefix="/api/v1", tags=["auth"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
async def root():
    """Root endpoint redirects to API docs."""
    return {"message": "SWAIF Clinic Follow-up System API", "docs": "/api/docs"}
