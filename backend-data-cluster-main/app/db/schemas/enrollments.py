enrollments_schema = {
  "properties": {
    "COURSE_CODE": {
      "bsonType": "string"
    },
    "SUBCLASS_CODE": {
      "bsonType": "string"
    },
    "QUOTA": {
      "bsonType": ["int", "null"]
    },
    "APPROVED_HEAD_COUNT": {
      "bsonType": ["int", "null"]
    },
    "LAST_UPDATED": {
      "bsonType": "date"
    },
  },
  "required": [
    "COURSE_CODE",
    "SUBCLASS_CODE"
  ]
}
enrollments_validator = {
  "$jsonSchema" : enrollments_schema
}
