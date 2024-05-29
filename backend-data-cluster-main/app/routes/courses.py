from fastapi import APIRouter, Request
from ..utils.data.create_objectid import create_objectid
from ..utils.datetime.hk_time_now import hk_time_now
from bson import ObjectId
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# Houses all endpoints related to retrieving course information
router = APIRouter(
  prefix="/courses",
  tags=["Courses"]
)

# Get all course information
@router.get("/get-all")
async def get_all(request: Request):
  courses = request.app.state.db.find_all("courses")
  for course in courses:
    del course["TNL"]
    # Data by default is stored as aggregated data, convert that data into an average
    course["RATING"] /= float(course["RATING_COUNT"])
    course["USEFULNESS"] /= float(course["RATING_COUNT"])
    course["GRADING"] /= float(course["RATING_COUNT"])
    course["WORKLOAD"] /= float(course["RATING_COUNT"])
    course["DIFFICULTY"] /= float(course["RATING_COUNT"])
  return courses

# Get information for a particular courses
@router.get("/get")
async def get(request: Request, course_code = "COMP3322"):
  course = request.app.state.db.find_one("courses", {"COURSE_CODE" : course_code})
  if "COURSE_CODE" in course:
    # Data by default is stored as aggregated data, convert that data into an average
    course["RATING"] /= float(course["RATING_COUNT"])
    course["USEFULNESS"] /= float(course["RATING_COUNT"])
    course["GRADING"] /= float(course["RATING_COUNT"])
    course["WORKLOAD"] /= float(course["RATING_COUNT"])
    course["DIFFICULTY"] /= float(course["RATING_COUNT"])
  return course

# Get all subclasses for a course and their enrollment information
@router.get("/get-subclasses")
async def get_subclasses(request: Request, course_code = "COMP3322"):
  subclasses = request.app.state.db.find("subclasses", {"COURSE_CODE" : course_code})
  enrollments = request.app.state.db.find("enrollments", {"COURSE_CODE" : course_code})
  data = {
    "SUBCLASSES" : subclasses,
    "ENROLLMENTS" : enrollments
  }
  return data

# Get sftl data for a course
@router.get("/get-sftl")
async def get_sftl(request: Request, course_code = "COMP3322"):
  sftl = request.app.state.db.find("sftl", {"COURSE_CODE" : course_code})
  return sftl

# Get all historical course records for a course
@router.get("/get-history")
async def get_history(request: Request, course_code = "COMP3322"):
  history = request.app.state.db.find("course_history", {"COURSE_CODE" : course_code})
  return history

# Get all historical records for all courses
@router.get("/get-all-history")
async def get_history(request: Request):
  history = request.app.state.db.find_all("course_history")
  return history

# Get all reviews for a course
@router.get("/get-reviews")
async def get_reviews(request: Request, course_code = "COMP3322"):
  reviews = request.app.state.db.find("course_reviews", {"COURSE_CODE" : course_code})
  # Filter out spam
  reviews = [review for review in reviews if review["COMMENT"] is not None and (not request.app.state.models.spam.is_spam(review["COMMENT"]))]
  for review in reviews:
    # For mocking purposes, this should be repeated for all courses when professor data is available
    if course_code == "COMP3322":
      prof = request.app.state.db.find_one("professors", {"PROF_ID" : create_objectid("atctam_cs")})
      review["PROF_ID_NAME_MAP"] = [{
        "PROF_ID" : prof["PROF_ID"],
        "PROF_NAME" : prof["FULLNAME"]
      }]
    # For mocking purposes, this should be repeated for all courses with relevant user data
    review["USER_DEPARTMENT"] = "Computer Science"
    review["USER_FACULTY"] = "Engineering"
    review["USER_PROFILE_PIC"] = "/user-profile-pics/profile-pic.svg"
  return reviews

# Get all reviews for a course made by a given user
@router.get("/get-reviews-by-user")
async def get_reviews_by_user(request: Request, course_code = "COMP3322", user_id = "5f94a577fcaee5e5f36dc0f1"):
  reviews = request.app.state.db.find("course_reviews", {"COURSE_CODE" : course_code, "USER_ID" : ObjectId(user_id)})
  for review in reviews:
    # For mocking purposes, this should be repeated for all courses when professor data is available
    if course_code == "COMP3322":
      prof = request.app.state.db.find_one("professors", {"PROF_ID" : create_objectid("atctam_cs")})
      review["PROF_ID_NAME_MAP"] = [{
        "PROF_ID" : prof["PROF_ID"],
        "PROF_NAME" : prof["FULLNAME"]
      }]
  return reviews

# Get all course and professor reviews for a given course made by a given user
@router.get("/get-all-reviews-by-user-and-course-code")
async def get_all_reviews_by_user_and_course_code(request: Request, course_code = "COMP3322", user_id = "5f94a577fcaee5e5f36dc0f1"):
  course_reviews = request.app.state.db.find("course_reviews", {"COURSE_CODE" : course_code, "USER_ID" : ObjectId(user_id)})
  prof_reviews = request.app.state.db.find("prof_reviews", {"COURSE_CODE" : course_code, "USER_ID" : ObjectId(user_id)})
  return {"COURSE_REVIEWS" : course_reviews, "PROF_REVIEWS" : prof_reviews}

# Mock data for docs page
review_model_test = {
  "COURSE_CODE": "COMP3322",
  "USER_ID": "5f94a577fcaee5e5f36dc0f1",
  "PROF_IDS": ["00000061746374616d5f6373"],
  "COMMENT": "This is a test comment",
  "RATING": 2,
  "DIFFICULTY": 1,
  "GRADING": 5,
  "USEFULNESS": 5,
  "WORKLOAD": 1,
  "IS_VERIFIED": False,
  "YEAR": "2023-24",
  "SEM": "1"
}

# Model of data sent when creating a review
class ReviewModel(BaseModel):
  COURSE_CODE : str
  USER_ID : str
  PROF_IDS : Optional[List[str]]
  COMMENT : str
  RATING : float 
  DIFFICULTY : float
  GRADING : float 
  USEFULNESS : float
  WORKLOAD : float 
  IS_VERIFIED : bool 
  YEAR : str 
  SEM : str
  model_config = ConfigDict(
    arbitrary_types_allowed=True,
    json_encoders={ObjectId: str},
    json_schema_extra={
      "example": review_model_test
    },
  )

# Create of update a review for a course
@router.post("/create-or-update-review")
async def create_or_update_review(request: Request, data : ReviewModel):
  given_review = BaseModel.model_dump(data)
  given_review["DATETIME"] = hk_time_now()
  given_review["USER_ID"] = ObjectId(given_review["USER_ID"])
  given_review["PROF_IDS"] = [ObjectId(prof_id) for prof_id in given_review["PROF_IDS"]]
  # Get the existing review if available
  review_from_collection = request.app.state.db.find_one("course_reviews", {"COURSE_CODE" : given_review["COURSE_CODE"], "USER_ID" : given_review["USER_ID"]})
  rating_count_inc = 0
  # If review is a new review, mock the old review
  if "COURSE_CODE" not in review_from_collection:
    review_from_collection = {
      "RATING" : 0,
      "USEFULNESS" : 0,
      "GRADING": 0, 
      "WORKLOAD" : 0, 
      "DIFFICULTY": 0, 
    }
    rating_count_inc = 1
  # Update the course metrics based on the given review
  course_update_obj = {"$inc" : {
    "RATING" : given_review["RATING"] - review_from_collection["RATING"],
    "USEFULNESS" : given_review["USEFULNESS"] - review_from_collection["USEFULNESS"],
    "GRADING" : given_review["GRADING"] - review_from_collection["GRADING"],
    "WORKLOAD" : given_review["WORKLOAD"] - review_from_collection["WORKLOAD"],
    "DIFFICULTY" : given_review["DIFFICULTY"] - review_from_collection["DIFFICULTY"],
    "RATING_COUNT" : rating_count_inc
  }}
  # Push the new review and the updated course data
  success_review = request.app.state.db.update_one("course_reviews", {"COURSE_CODE" : given_review["COURSE_CODE"], "USER_ID" : given_review["USER_ID"]}, given_review, True)
  success_course = request.app.state.db.update_one_with_custom_fields("courses", {"COURSE_CODE" : given_review["COURSE_CODE"]}, course_update_obj) if success_review else False
  return success_course and success_review

# Delete a given review
@router.delete("/delete-review")
async def delete_review(request: Request, id : str):
  # Fetch the review to be deleted
  review = request.app.state.db.find_one("course_reviews", {"_id" : ObjectId(id)})
  success_review = request.app.state.db.delete_one("course_reviews", {"_id" : ObjectId(id)})
  # Update the course metrics by removing the metrics from the deleted review
  course_update_obj = {"$inc" : {
    "RATING" : 0 - review["RATING"], 
    "USEFULNESS" : 0 - review["USEFULNESS"], 
    "GRADING": 0 - review["GRADING"], 
    "WORKLOAD" : 0 - review["WORKLOAD"], 
    "DIFFICULTY": 0 - review["DIFFICULTY"], 
    "RATING_COUNT" : 0 - 1, 
  }}
  success_course = request.app.state.db.update_one_with_custom_fields("courses", {"COURSE_CODE" : review["COURSE_CODE"]}, course_update_obj) if success_review else False
  return success_course and success_review