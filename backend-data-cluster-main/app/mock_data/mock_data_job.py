from .course_reviews import mock_course_reviews
from .prof_reviews import mock_prof_reviews
from pymongo import UpdateOne

# Pushes mock data to the DB collections
def push_mock_data(logger, db):
  try:
    logger.info("Pushing mock reviews to database.")
    course_reviews = mock_course_reviews
    course_reviews_update_operations = [
      UpdateOne(
          {"USER_ID": obj["USER_ID"], "COURSE_CODE" : obj["COURSE_CODE"]},
          {"$set": obj},
          upsert=True
      )
      for obj in course_reviews
    ]
    db.bulk_write('course_reviews', course_reviews_update_operations)
    prof_reviews = mock_prof_reviews
    prof_reviews_update_operations = [
      UpdateOne(
          {"USER_ID": obj["USER_ID"], "COURSE_CODE" : obj["COURSE_CODE"]},
          {"$set": obj},
          upsert=True
      )
      for obj in prof_reviews
    ]
    db.bulk_write('prof_reviews', prof_reviews_update_operations)
  except Exception as ex:
    logger.error(ex)