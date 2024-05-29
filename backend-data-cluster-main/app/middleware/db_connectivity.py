from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.encoders import jsonable_encoder

# Returns an incvalid response if DB is not connected
from fastapi.responses import JSONResponse
class DBMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = JSONResponse(
            jsonable_encoder(
                {'body' : None, 'err' : "Database connection unsucessful."}
            )
        )
        if (request.app.state.db.connection_status):
            response = await call_next(request)
        else:
            request.app.state.db.connect() # Attempt reconnection
            if (request.app.state.db.connection_status):
                response = await call_next(request)
            request.app.state.logger.info(
                "DB Middleware: Database is not connected.",
            )
        return response