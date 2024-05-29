subclasses_schema = {
  "properties": {
    "SUBCLASS_CODE": {
      "bsonType": "string"
    },
    "COURSE_CODE": {
      "bsonType": "string"
    },
    "YEAR": {
      "bsonType": "string"
    },
    "SEM": {
      "bsonType": "string"
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
    },
    "INSTRUCTORS_PLACEHOLDER": {
      "bsonType": "string",
    },
    "SUBCLASS": {
      "bsonType": "string"
    },
    "TIMINGS": {
      "bsonType": "array",
      "items": {
        "bsonType": "object",
        "properties": {
          "DAY": {
            "bsonType": "string"
          },
          "VENUE": {
            "bsonType": ["string", "null"]
          },
          "START_TIME": {
            "bsonType": "string"
          },
          "END_TIME": {
            "bsonType": "string"
          }
        }
      }
    }
  },
  "required": [
    "SUBCLASS_CODE",
    "COURSE_CODE",
    "SUBCLASS"
  ]
}
subclasses_validator = {
  "$jsonSchema" : subclasses_schema
}
