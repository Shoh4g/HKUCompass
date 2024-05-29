from pymongo import ReplaceOne

# Writes dat to the DB
def write(db, logger, data):
  profs_insertion_list = map_insertion_list(prof_replace_obj, data)
  db.bulk_write("professors", profs_insertion_list)

# Makes a list of objects for bulk writing
def map_insertion_list(mapper, list):
  mapped_list = []
  for l in list:
    mapped_list.append(mapper(l))
  return mapped_list

def prof_replace_obj(prof):
  return ReplaceOne({"PROF_ID" : prof["PROF_ID"]}, prof, upsert=True)