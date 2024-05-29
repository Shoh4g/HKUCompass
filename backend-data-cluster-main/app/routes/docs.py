from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

router = APIRouter()
security = HTTPBasic()

# For password authentication
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.getenv("DOC_USERNAME"))
    correct_password = secrets.compare_digest(credentials.password, os.getenv("DOC_PASSWORD"))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Returns the docs page from swagger docs
@router.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

# We can use a docs page from redoc as well if need be
# @router.get("/redoc", include_in_schema=False)
# async def get_redoc_documentation(username: str = Depends(get_current_username)):
#     return get_redoc_html(openapi_url="/openapi.json", title="docs")
