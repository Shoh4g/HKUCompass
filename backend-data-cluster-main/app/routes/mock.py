from fastapi import APIRouter, Request, BackgroundTasks
import datetime
from ..mock_data.mock_data_job import push_mock_data

# Endpoints to trigger the pushing of mock data to the DB
router = APIRouter(
  prefix="/mock",
  tags=["Mock Data"]
)

# Push mock reviews to the DB
@router.get("/push-mock-reviews")
async def push_mock_reviews(request: Request, background_tasks: BackgroundTasks):
  time = str(datetime.datetime.now())
  background_tasks.add_task(push_mock_data, request.app.state.logger, request.app.state.db)
  return "Task started at time " + time + ", check server logs for state."