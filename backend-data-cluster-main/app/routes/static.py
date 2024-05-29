from fastapi import APIRouter
from fastapi.responses import FileResponse

# Serves all static pages
router = APIRouter(
  prefix="/static",
  tags=["Static"]
)

# Static page for testing transcript parsing functionality
@router.get("/upload-transcript-info")
async def serve_html():
  return FileResponse("app/static/upload_transcript_info.html")