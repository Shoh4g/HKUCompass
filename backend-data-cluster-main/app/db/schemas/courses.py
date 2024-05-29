courses_schema = {
  "properties": {
    "COURSE_CODE": {
      "bsonType": "string"
    },
    "COURSE_TITLE": {
      "bsonType": "string"
    },
    "CREDITS": {
      "bsonType": "int"
    },
    "FACULTY": {
      "bsonType": "string"
    },
    "ENROLLMENT_REQUIREMENTS": {
      "bsonType": [ "null", "string" ]
    },
    "COURSE_DESCRIPTION": {
      "bsonType": "string"
    },
    "RATING": {
      "bsonType": "double"
    },
    "USEFULNESS": {
      "bsonType": "double"
    },
    "WORKLOAD": {
      "bsonType": "double"
    },
    "GRADING": {
      "bsonType": "double"
    },
    "DIFFICULTY": {
      "bsonType": "double"
    },
    "RATING_COUNT": {
      "bsonType": "int"
    },
    "TNL": {
      "bsonType": "array",
      "items": {
        "bsonType": "object",
        "properties": {
          "DETAIL": {
            "bsonType": "string"
          },
          "SHARE": {
            "bsonType": "double"
          },
          "PERCENTAGE": {
            "bsonType": "double"
          }
        }
      }
    }
  },
  "required": [
    "COURSE_CODE",
    "COURSE_TITLE"
  ]
}
courses_validator = {
  "$jsonSchema" : courses_schema
}
