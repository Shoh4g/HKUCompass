from bson import ObjectId
from ..utils.datetime.random_date import random_date_last_six_months
import random

def generate_random_number(x, y):
  return float(random.randint(x, y))

# Mock course reviews for COMP3322
mock_course_reviews = [
  {
    "COMMENT": "Great practical approach! Loved getting hands-on experience with web development languages like PHP and JavaScript.",
    "COURSE_CODE": "COMP3322",
    "DATETIME": random_date_last_six_months(),
    "DIFFICULTY": generate_random_number(1, 5),
    "GRADING": generate_random_number(1, 5),
    "HELPFUL": random.randint(5, 25),
    "IS_VERIFIED": True,
    "NOT_HELPFUL": random.randint(5, 25),
    "PROF_IDS": [
      ObjectId("00000061746374616d5f6373")
    ],
    "RATING": generate_random_number(1, 5),
    "SEM": "1",
    "USEFULNESS": generate_random_number(1, 5),
    "USER_ID": ObjectId("5f94a577fcaee5e5f36dc0f1"),
    "WORKLOAD": generate_random_number(1, 5),
    "YEAR": "2023-24"
  },
  {
    "COMMENT": "Appreciated the emphasis on staying current with industry trends. Learning about HTML5 and web services was particularly insightful.",
    "COURSE_CODE": "COMP3322",
    "DATETIME": random_date_last_six_months(),
    "DIFFICULTY": generate_random_number(1, 5),
    "GRADING": generate_random_number(1, 5),
    "HELPFUL": random.randint(5,25),
    "IS_VERIFIED": True,
    "NOT_HELPFUL": random.randint(5, 25),
    "PROF_IDS": [
      ObjectId("00000061746374616d5f6373")
    ],
    "RATING": generate_random_number(1, 5),
    "SEM": "1",
    "USEFULNESS": generate_random_number(1, 5),
    "USER_ID": ObjectId("5f94a577fcaee5e5f36dc0f2"),
    "WORKLOAD": generate_random_number(1, 5),
    "YEAR": "2023-24"
  },
  {
    "COMMENT": "Wished there was more focus on theoretical concepts behind internet protocols. Understanding the fundamentals would've been beneficial.",
    "COURSE_CODE": "COMP3322",
    "DATETIME": random_date_last_six_months(),
    "DIFFICULTY": generate_random_number(1, 5),
    "GRADING": generate_random_number(1, 5),
    "HELPFUL": random.randint(5, 25),
    "IS_VERIFIED": False,
    "NOT_HELPFUL": random.randint(5, 25),
    "PROF_IDS": [
      ObjectId("00000061746374616d5f6373")
    ],
    "RATING": generate_random_number(1, 5),
    "SEM": "1",
    "USEFULNESS": generate_random_number(1, 5),
    "USER_ID": ObjectId("5f94a577fcaee5e5f36dc0f3"),
    "WORKLOAD": generate_random_number(1, 5),
    "YEAR": "2023-24"
  },
  {
    "COMMENT": "Found the heavy reliance on continuous assessment a bit overwhelming. It felt like a constant pressure to perform.",
    "COURSE_CODE": "COMP3322",
    "DATETIME": random_date_last_six_months(),
    "DIFFICULTY": generate_random_number(1, 5),
    "GRADING": generate_random_number(1, 5),
    "HELPFUL": random.randint(5, 25),
    "IS_VERIFIED": True,
    "NOT_HELPFUL": random.randint(5, 25),
    "PROF_IDS": [
      ObjectId("00000061746374616d5f6373")
    ],
    "RATING": generate_random_number(1, 5),
    "SEM": "1",
    "USEFULNESS": generate_random_number(1, 5),
    "USER_ID": ObjectId("5f94a577fcaee5e5f36dc0f4"),
    "WORKLOAD": generate_random_number(1, 5),
    "YEAR": "2023-24"
  },
  {
    "COMMENT": "Meh, didn't like it.",
    "COURSE_CODE": "COMP3322",
    "DATETIME": random_date_last_six_months(),
    "DIFFICULTY": generate_random_number(1, 5),
    "GRADING": generate_random_number(1, 5),
    "HELPFUL": random.randint(5, 25),
    "IS_VERIFIED": False,
    "NOT_HELPFUL": random.randint(5, 25),
    "PROF_IDS": [
      ObjectId("00000061746374616d5f6373")
    ],
    "RATING": generate_random_number(1, 5),
    "SEM": "1",
    "USEFULNESS": generate_random_number(1, 5),
    "USER_ID": ObjectId("5f94a577fcaee5e5f36dc0f5"),
    "WORKLOAD": generate_random_number(1, 5),
    "YEAR": "2023-24"
  },
  {
    "COMMENT": "Boring course.",
    "COURSE_CODE": "COMP3322",
    "DATETIME": random_date_last_six_months(),
    "DIFFICULTY": generate_random_number(1, 5),
    "GRADING": generate_random_number(1, 5),
    "HELPFUL": random.randint(5, 25),
    "IS_VERIFIED": False,
    "NOT_HELPFUL": random.randint(5, 25),
    "PROF_IDS": [
      ObjectId("00000061746374616d5f6373")
    ],
    "RATING": generate_random_number(1, 5),
    "SEM": "1",
    "USEFULNESS": generate_random_number(1, 5),
    "USER_ID": ObjectId("5f94a577fcaee5e5f36dc0f6"),
    "WORKLOAD": generate_random_number(1, 5),
    "YEAR": "2023-24"
  },
  {
    "COMMENT": "The course had a very high workload.",
    "COURSE_CODE": "COMP3322",
    "DATETIME": random_date_last_six_months(),
    "DIFFICULTY": generate_random_number(1, 5),
    "GRADING": generate_random_number(1, 5),
    "HELPFUL": random.randint(5, 25),
    "IS_VERIFIED": False,
    "NOT_HELPFUL": random.randint(5, 25),
    "PROF_IDS": [
      ObjectId("00000061746374616d5f6373")
    ],
    "RATING": generate_random_number(1, 5),
    "SEM": "1",
    "USEFULNESS": generate_random_number(1, 5),
    "USER_ID": ObjectId("5f94a577fcaee5e5f36dc0f7"),
    "WORKLOAD": generate_random_number(1, 5),
    "YEAR": "2023-24"
  }
]