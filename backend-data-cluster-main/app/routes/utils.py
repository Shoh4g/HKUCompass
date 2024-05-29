from fastapi import APIRouter, Request, BackgroundTasks
from ..data.courses_job import general_courses_job
from ..data.profs_job.engineering.cs import collect as csCollect
from ..utils.data.create_driver import create_driver
import datetime

router = APIRouter(
  prefix="/utils",
  tags=["Utility Functions"]
)

@router.get("/trigger-general-courses-job")
async def trigger_general_courses_job(request : Request, background_tasks : BackgroundTasks): 
  time = str(datetime.datetime.now())
  background_tasks.add_task(general_courses_job, request.app.state.logger, request.app.state.db)
  return "Job started at time " + time + ", check server logs for state."

@router.get("/trigger-prof-job-cs")
async def trigger_prof_job_cs(request : Request, background_tasks : BackgroundTasks): 
  time = str(datetime.datetime.now())
  background_tasks.add_task(csCollect, request.app.state.db, request.app.state.logger, create_driver())
  return "Job started at time " + time + ", check server logs for state."

@router.get("/clear-collection-courses")
async def clear_collection_courses(request : Request, background_tasks : BackgroundTasks): 
  s = request.app.state.db.clear('courses')
  return "The collection 'courses' was cleared." if s else "The collection 'courses' was not cleared, check error logs for details."

@router.get("/clear-collection-course-reviews")
async def clear_collection_course_reviews(request : Request, background_tasks : BackgroundTasks): 
  s = request.app.state.db.clear('course_reviews')
  return "The collection 'course_reviews' was cleared." if s else "The collection 'course_reviews' was not cleared, check error logs for details."

@router.get("/clear-collection-course-history")
async def clear_collection_course_reviews(request : Request, background_tasks : BackgroundTasks): 
  s = request.app.state.db.clear('course_history')
  return "The collection 'course_history' was cleared." if s else "The collection 'course_history' was not cleared, check error logs for details."

@router.get("/clear-collection-subclasses")
async def clear_collection_subclasses(request : Request, background_tasks : BackgroundTasks): 
  s = request.app.state.db.clear('subclasses')
  return "The collection 'subclasses' was cleared." if s else "The collection 'subclasses' was not cleared, check error logs for details."

@router.get("/clear-collection-enrollments")
async def clear_collection_enrollments(request : Request, background_tasks : BackgroundTasks): 
  s = request.app.state.db.clear('enrollments')
  return "The collection 'enrollments' was cleared." if s else "The collection 'enrollments' was not cleared, check error logs for details."

@router.get("/clear-collection-professors")
async def clear_collection_professors(request : Request, background_tasks : BackgroundTasks): 
  s = request.app.state.db.clear('professors')
  return "The collection 'professors' was cleared." if s else "The collection 'professors' was not cleared, check error logs for details."

@router.get("/clear-collection-prof-reviews")
async def clear_collection_professor_reviews(request : Request, background_tasks : BackgroundTasks): 
  s = request.app.state.db.clear('prof_reviews')
  return "The collection 'prof_reviews' was cleared." if s else "The collection 'prof_reviews' was not cleared, check error logs for details."

@router.get("/clear-collection-sftl")
async def clear_collection_sftl(request : Request, background_tasks : BackgroundTasks): 
  s = request.app.state.db.clear('sftl')
  return "The collection 'sftl' was cleared." if s else "The collection 'sftl' was not cleared, check error logs for details."

@router.get("/clear-collection-users")
async def clear_collection_sftl(request : Request, background_tasks : BackgroundTasks): 
  s = request.app.state.db.clear('users')
  return "The collection 'users' was cleared." if s else "The collection 'users' was not cleared, check error logs for details."

@router.get("/get-all-subject-areas")
async def get_all_subject_areas(request : Request):
  courses = request.app.state.db.find_all("courses")
  sub_area_map = {course["COURSE_CODE"][0:4] : None for course in courses}
  sub_areas = [key for key in sub_area_map]
  return sub_areas