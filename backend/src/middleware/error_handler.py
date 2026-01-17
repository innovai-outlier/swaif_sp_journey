"""
Error handling middleware for FastAPI.
Provides consistent error responses and logging.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from backend.src.config.logging import get_logger
import traceback


logger = get_logger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """
    Middleware to handle errors consistently across the application.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/route handler
        
    Returns:
        Response with error details if an exception occurs
    """
    try:
        response = await call_next(request)
        return response
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Validation Error",
                "message": str(e)
            }
        )
    except PermissionError as e:
        logger.warning(f"Permission denied: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "error": "Permission Denied",
                "message": str(e)
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred"
            }
        )
