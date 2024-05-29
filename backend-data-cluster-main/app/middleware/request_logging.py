from starlette.middleware.base import BaseHTTPMiddleware

# Logs all incoming requests
class ReqLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        extra={
            "req" : { "method" : request.method, "url" : str(request.url) },
            "res" : { "status_code" : response.status_code }
        },
        request.app.state.logger.info(
            "Incoming request: " + str(extra)
        )
        return response