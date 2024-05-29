from ..logs.logger import get_logger
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
from io import StringIO

# Unisersal Exception Handler for the server
logger = get_logger()
class CatchExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as http_exception:
            return JSONResponse(
                status_code=http_exception.status_code,
                content={"error": "Client Error", "message": str(http_exception.detail)},
            )
        except Exception as e:
            traceback_buffer = StringIO()
            traceback.print_exc(file=traceback_buffer)
            traceback_str = traceback_buffer.getvalue()
            logger.error(traceback_str)
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error", "message": str(e)},
            )