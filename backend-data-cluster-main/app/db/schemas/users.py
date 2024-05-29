users_schema = {
  "properties": {
    "EMAIL": {
      "bsonType": "string"
    },
    "FULLNAME": {
      "bsonType": "string"
    },
    "DEPARTMENT": {
      "bsonType": "string"
    },
    "FACULTY": {
      "bsonType": "string"
    },
    "PROFILE_PIC": {
      "bsonType": "string"
    },
    "PASSWORD": {
      "bsonType": "string"
    },
    "YEAR_OF_STUDY": {
      "bsonType": "string"
    },
    "MAJORS": {
      "bsonType": "array",
      "items": {
        "bsonType": "string"
      }
    },
    "MINORS": {
      "bsonType": "array",
      "items": {
        "bsonType": "string"
      }
    },
    "DEGREE": {
      "bsonType": "string"
    }, 
    "IS_ONBOARDED": {
      "bsonType": "bool"
    },
    "COURSE_HISTORY": {
      "bsonType": "array",
      "items": {
        "bsonType": "object",
        "properties": {
          "COURSE_CODE": {
            "bsonType": "string"
          },
          "YEAR": {
            "bsonType": "string"
          },
          "SEM": {
            "bsonType": "string"
          },
          "IS_REVIEWED": {
            "bsonType" : "bool"
          }
        }
      }
    },
    "BOOKMARKS": {
      "bsonType": "array",
      "items": {
        "bsonType": "string"
      }
    },
    "CART": {
      "bsonType": "array",
      "items": {
        "bsonType": "string"
      }
    },
    "HELPFUL_REVIEWS": {
      "bsonType": "array",
      "items": {
        "bsonType": "objectId"
      }
    },
    "NOT_HELPFUL_REVIEWS": {
      "bsonType": "array",
      "items": {
        "bsonType": "objectId"
      }
    },
  },
  "required": [
    "EMAIL"
  ]
}
users_validator = {
  "$jsonSchema" : users_schema
}
