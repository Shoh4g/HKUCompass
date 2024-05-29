from .engineering import job as enggJob

async def profs_job(db, logger):
  enggJob(db, logger)