from fastapi import APIRouter, Request, HTTPException

# Testing routes
router = APIRouter(
  prefix="/test",
  tags=["Testing"]
)

# Basic hello world test
@router.get("/hello-world")
async def hello_world():
  return "Hello World!"

# Check if DB is connected
@router.get("/db-connectivity")
async def db_connectivity(request: Request):
  return request.app.state.db.connection_status

# Check exception handling for a general exception
@router.get("/exception_handling")
async def exception_handling():
  raise Exception("This is a test")

# Check exception handling for HTTPException
@router.get("/http_exception_handling")
async def exception_handling():
  raise HTTPException("This is a test")