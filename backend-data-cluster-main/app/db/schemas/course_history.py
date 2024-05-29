course_history_schema = {
  "properties": {
    "COURSE_CODE": {
      "bsonType": "string"
    },
    "STRM": {
      "bsonType": "string"
    },
    "YEAR": {
      "bsonType": "string"
    },
    "SEM": {
      "bsonType": "string"
    },
    "INSTRUCTORS_PLACEHOLDER": {
      "bsonType": "string",
    },
    "INSTRUCTORS": {
      "bsonType": "array",
      "items": {
        "bsonType": "object",
        "properties": {
          "NAME": {
            "bsonType": "string"
          },
          "PROF_ID": {
            "bsonType": "objectId"
          },
        }
      }
    }
  },
  "required": [
    "STRM",
    "COURSE_CODE"
  ]
}
course_history_validator = {
  "$jsonSchema" : course_history_schema
}
