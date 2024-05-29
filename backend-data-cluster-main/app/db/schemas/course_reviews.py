course_reviews_schema = {
  "properties": {
    "COURSE_CODE": {
      "bsonType": "string"
    },
    "USER_ID": {
      "bsonType": "objectId"
    },
    "PROF_IDS": {
      "bsonType": "array",
      "items": {
        "bsonType": "objectId"
      }
    },
    "COMMENT": {
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
    "DATETIME": {
      "bsonType": "date"
    },
    "IS_VERIFIED": {
      "bsonType": "bool"
    },
    "YEAR": {
      "bsonType": "string"
    },
    "SEM": {
      "bsonType": "string"
    },
    "HELPFUL": {
      "bsonType": "int"
    },
    "NOT_HELPFUL": {
      "bsonType": "int"
    }
  },
  "required": [
    "COURSE_CODE",
    "USER_ID",
    "PROF_IDS",
    "USEFULNESS",
    "WORKLOAD",
    "GRADING",
    "DIFFICULTY",
    "DATETIME"
  ]
}
course_reviews_validator = {
  "$jsonSchema" : course_reviews_schema
}
