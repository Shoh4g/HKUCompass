from ....utils.data.create_driver import create_driver
from .cs import collect as csCollect

def job(db, logger):
  logger.info("ENGG Job: Starting ENGG Job.")
  driver = create_driver()
  csCollect(db, logger, driver)
