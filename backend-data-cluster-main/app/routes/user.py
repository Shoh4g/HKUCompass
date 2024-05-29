from fastapi import APIRouter, Request, UploadFile
from bson import ObjectId
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from bson import ObjectId

# Routes for handling User Data
router = APIRouter(
  prefix="/user",
  tags=["User Data"]
)

# Get all data for a given user
@router.get("/get-user-data")
async def get_user_data(request: Request, email = "test@hku.hk"):
  user = request.app.state.db.find_one("users", {"EMAIL" : email})
  return user

# Get all spam reviews a user has left
@router.get("/get-spam-reviews")
async def get_user_data(request: Request, user_id = "5f94a577fcaee5e5f36dc0f6"):
  course_reviews = request.app.state.db.find("course_reviews", {"USER_ID" : ObjectId(user_id)})
  prof_reviews = request.app.state.db.find("prof_reviews", {"USER_ID" : ObjectId(user_id)})
  course_reviews = [review for review in course_reviews if review["COMMENT"] is not None and request.app.state.models.spam.is_spam(review["COMMENT"])]
  prof_reviews = [review for review in prof_reviews if review["COMMENT"] is not None and request.app.state.models.spam.is_spam(review["COMMENT"])]
  return {"COURSE_REVIEWS" : course_reviews, "PROF_REVIEWS" : prof_reviews}

# Get all course reviews a user has left
@router.get("/get-course-reviews")
async def get_user_data(request: Request, user_id = "5f94a577fcaee5e5f36dc0f6"):
  course_reviews = request.app.state.db.find("course_reviews", {"USER_ID" : ObjectId(user_id)})
  return course_reviews

# Get all professor reviews a user has left
@router.get("/get-prof-reviews")
async def get_user_data(request: Request, user_id = "5f94a577fcaee5e5f36dc0f6"):
  prof_reviews = request.app.state.db.find("prof_reviews", {"USER_ID" : ObjectId(user_id)})
  return prof_reviews

# Mock data for the docs page
user_model_test = {
  "EMAIL" : "test@hku.hk",
  "IS_ONBOARDED" : False
}

# A model for course history
class CourseHistoryModel(BaseModel):
  COURSE_CODE : str
  YEAR : str
  SEM : str
  IS_REVIEWED : Optional[bool]

# A model to update user data
class UserUpdateModel(BaseModel):
  EMAIL : str
  FULLNAME : Optional[str] = None
  DEGREE : Optional[str] = None
  YEAR_OF_STUDY : Optional[str] = None 
  MAJORS : Optional[List[str]] = None
  MINORS : Optional[List[str]]  = None
  COURSE_HISTORY : Optional[List[CourseHistoryModel]] = None
  BOOKMARKS : Optional[List[str]] = None
  CART : Optional[List[str]] = None
  HELPFUL_REVIEWS : Optional[str] = None
  NOT_HELPFUL_REVIEWS : Optional[str] = None
  IS_ONBOARDED : Optional[bool] = None
  model_config = ConfigDict(
    arbitrary_types_allowed = True,
    json_encoders={ObjectId: str},
    json_schema_extra={
      "example": user_model_test
    },
  )

# Updates user data
@router.post("/update-user-data")
async def update_user_data(request: Request, user : UserUpdateModel):
  user = BaseModel.model_dump(user)
  # Delete all optional keys which are not given in the body of the post request
  keys = [key for key in user]
  for key in keys:
    if user[key] is None:
      del user[key]
  success = request.app.state.db.update_one("users", {"EMAIL" : user["EMAIL"]}, user)
  user = request.app.state.db.find_one("users", {"EMAIL" : user["EMAIL"]})
  return {"SUCCESS" : success, "USER" : user}

# Parses the transcipt of a user
@router.post("/get-transcript-info")
async def set_transcript_info(request: Request, pdf_file: UploadFile):
  contents = await pdf_file.read()
  parsed_pdf = request.app.state.models.transcript_parser(contents)
  courses = parsed_pdf["Courses"]
  course_history = [{
      "COURSE_CODE" : course["Course Code"].replace(" ", ""),
      "YEAR" : course["Term"].split(" ")[0],
      "SEM" : course["Grade"]
    } for course in courses]
  return course_history