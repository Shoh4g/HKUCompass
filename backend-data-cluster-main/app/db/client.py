
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os, uuid
from .schemas.professors import professors_validator
from .schemas.courses import courses_validator
from .schemas.course_history import course_history_validator
from .schemas.prof_reviews import prof_reviews_validator
from .schemas.course_reviews import course_reviews_validator
from .schemas.enrollments import enrollments_validator
from .schemas.sftl import sftl_validator
from .schemas.subclasses import subclasses_validator
from .schemas.users import users_validator
from ..logs.logger import logger
from bson.json_util import dumps
import json

# A class for the client for the DB connection
class MongoDBClient:
  def __init__(self, name = str(uuid.uuid1)):
    self.name = name
    self.uri = str(os.getenv("MONGODB_URI"))
    self.client = MongoClient(self.uri, server_api=ServerApi('1'))
    self.connection_status = False
    self.db = str(os.getenv("DB"))
    logger.info("Database client " + self.name + ": Database being used is " + str(self.db))
    self.connect()

  def __del__(self):
    self.close()

  # Attempts to connect to DB
  def connect(self):
    try:
      if not self.connection_status:
        self.client.admin.command('ping')
        logger.info("Database client " + self.name + ": Pinged the deployment. Successfully connected to MongoDB.")
        self.connection_status = True
        self.add_schemas()
    except Exception as e:
      logger.error("Database client " + self.name + ": Error in connecting to MongoDB. Error: " + str(e))
      self.connection_status = False

  # Closes DB connection
  def close(self):
    self.client.close()
    logger.info("Database client " + self.name + ": Database connection closed.")

  # Adds schemas to all collections of the DB 
  def add_schemas(self):
    db = self.client[self.db]
    collection_names = ['course_reviews', 'courses', 'enrollments', 'prof_reviews', 'professors', 'sftl', 'subclasses', 'users', 'course_history']
    collection_validators = [course_reviews_validator, courses_validator, enrollments_validator, prof_reviews_validator, professors_validator, sftl_validator, subclasses_validator, users_validator, course_history_validator]
    for i, name in enumerate(collection_names):
      try:
        res = db.command("collMod", name, validator = collection_validators[i])
        if (not res["ok"]):
          logger.error("Database client " + self.name + ": Error in adding schema to the " + name + " collection. MongoDB responsed with ok = 0.0")
      except Exception as e:
          logger.error("Database client " + self.name + ": Error in adding schema to the " + name + " collection. Error: " + str(e))

  # Performs a list of writes/updates to a given collection
  def bulk_write(self, collection, ops_array):
    db = self.client[self.db]
    try:
      col = db[collection]
    except Exception as e:
      logger.error("Database client " + self.name + ": Could not find collection " + collection + ". Error: " + str(e))
      return False
    try:
      col.bulk_write(ops_array)
      logger.info("Database client " + self.name + ": Bulk writing to collection: " + collection + " completed successfully.")
      return True
    except Exception as e:
      logger.error("Database client " + self.name + ": Error while bulk writing to collection: " + collection + ". Error: " + str(e))
      return False
  
  # Returns all objects in the collection
  def find_all(self, collection):
    db = self.client[self.db]
    try:
      col = db[collection]
    except Exception as e:
      logger.error("Database client " + self.name + ": Could not find collection: " + collection + ". Error: " + str(e))
      return []
    try:
      res = col.find({})
      data = json.loads(dumps(res))
      return data
    except Exception as e:
      logger.error("Database client " + self.name + ": Error in operation finding all objects from collection: " + collection + ". Error: " + str(e))
      return []
  
  # Finds a list of objects from a given collection given a list of filters
  def find(self, collection, filter_obj):
    db = self.client[self.db]
    try:
      col = db[collection]
    except Exception as e:
      logger.error("Database client " + self.name + ": Could not find collection: " + collection + ". Error: " + str(e))
      return []
    try:
      res = col.find(filter_obj)
      data = json.loads(dumps(res))
      return data
    except Exception as e:
      logger.error("Database client " + self.name + ": Error in operation finding all objects from collection: " + collection + ". Error: " + str(e))
      return []

  # Returns an object from the collection given a list of filters
  def find_one(self, collection, filter_obj):
    db = self.client[self.db]
    try:
      col = db[collection]
    except Exception as e:
      logger.error("Database client " + self.name + ": Could not find collection: " + collection + ". Error: " + str(e))
      return {}
    try:
      res = col.find_one(filter_obj)
      data = json.loads(dumps(res))
      return data if data is not None else {}
    except Exception as e:
      logger.error("Database client " + self.name + ": Error in operation finding one object from collection: " + collection + ". Error: " + str(e))
      return {}

  # Removes all objects from the collection
  def clear(self, collection):
    db = self.client[self.db]
    try:
      col = db[collection]
    except Exception as e:
      logger.error("Database client " + self.name + ": Could not find collection: " + collection + ". Error: " + str(e))
      return False
    try:
      col.delete_many({})
      return True
    except Exception as e:
      logger.error("Database client " + self.name + ": Error in operation deleting all objects from collection: " + collection + ". Error: " + str(e))
      return False

  # Deletes a given object from the collection based on the given filters
  def delete_one(self, collection, filter_obj):
    db = self.client[self.db]
    try:
      col = db[collection]
    except Exception as e:
      logger.error("Database client " + self.name + ": Could not find collection: " + collection + ". Error: " + str(e))
      return False
    try:
      col.delete_one(filter_obj)
      return True
    except Exception as e:
      logger.error("Database client " + self.name + ": Error in operation deleting object from collection: " + collection + ". Error: " + str(e))
      return False

  # Updates an object to the given data based on a list of filters
  def update_one(self, collection, filter_obj, new_data, upsert = False):
    db = self.client[self.db]
    try:
      col = db[collection]
    except Exception as e:
      logger.error("Database client " + self.name + ": Could not find collection: " + collection + ". Error: " + str(e))
      return False
    try:
      result = col.update_one(filter_obj, {"$set": new_data}, upsert)
      return True
    except Exception as e:
      logger.error("Database client " + self.name + ": Error in updating object in collection: " + collection + ". Error: " + str(e))
      return False

  # Updates on object based on the given update comments and list of filters 
  def update_one_with_custom_fields(self, collection, filter_obj, update_obj, upsert = False):
    db = self.client[self.db]
    try:
      col = db[collection]
    except Exception as e:
      logger.error("Database client " + self.name + ": Could not find collection: " + collection + ". Error: " + str(e))
      return False
    try:
      result = col.update_one(filter_obj, update_obj, upsert)
      return True
    except Exception as e:
      logger.error("Database client " + self.name + ": Error in updating object in collection: " + collection + ". Error: " + str(e))
      return False
