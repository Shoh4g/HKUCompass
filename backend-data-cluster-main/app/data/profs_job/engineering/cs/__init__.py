from .professors import collect_prof_data
from .db import write

# The main collection job for CS professors
def collect(db, logger, driver):
  global last_profs
  logger.info("Starting CS Job")
  prof_data = collect_prof_data(driver, logger)
  logger.info("Prof data collected for CS")
  last_profs = prof_data
  # Push to db
  logger.info("Prof data for CS: starting write")
  write(db, logger, prof_data)
  logger.info("CS Job completed")

