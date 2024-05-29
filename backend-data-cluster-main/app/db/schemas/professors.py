professors_schema = {
  "title": "professors",
  "properties": {
    "PROF_ID": {
      "bsonType": "objectId"
    },
    "FULLNAME": {
      "bsonType": "string"
    },
    "EMAIL": {
      "bsonType": "string"
    },
    "PROFILE_LINK": {
      "bsonType": "string"
    },
    "FACULTY": {
      "bsonType": "string"
    },
    "DEPARTMENT": {
      "bsonType": "string"
    },
    "ENGAGEMENT": {
      "bsonType": "double"
    },
    "CLARITY": {
      "bsonType": "double"
    },
    "RATING": {
      "bsonType": "double"
    },
    "RATING_COUNT": {
      "bsonType": "int"
    }
  },
  "required": [
    "PROF_ID",
    "FULLNAME",
    "EMAIL",
    "PROFILE_LINK",
    "FACULTY"
  ]
}
professors_validator = {
  "$jsonSchema" : professors_schema
}
