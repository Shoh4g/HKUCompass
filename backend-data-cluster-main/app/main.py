from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from .routes import courses
from .middleware.catch_exceptions import CatchExceptionsMiddleware
from .middleware.request_logging import ReqLogMiddleware
from .logs.logger import get_logger
from .middleware.db_connectivity import DBMiddleware
from .db.client import MongoDBClient
from .routes import test, courses, docs, utils, mock, auth, user, professors, ml, static
from .data.data_collection_job import DataJob
from .models.ml_models import MLModels

# Load project environment
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# Set up logging, database, data collection service, and ml models
logger = get_logger()
server_db_instance = MongoDBClient(name='SERVER-DB')
data_collection_job = DataJob(logger, server_db_instance)
ml_models = MLModels(server_db_instance)

# Load server context
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger = logger
    app.state.logger.info("Creating Server Context.")
    app.state.db = server_db_instance
    app.state.models = ml_models
    app.state.logger.info("Created Server Context sucessfully.")
    data_collection_job.run()
    yield
    app.state.db.close()
    data_collection_job.stop()
    app.state.logger.info("Server stopped successfully.")

# Main server app
app = FastAPI(lifespan = lifespan,     
            docs_url = None,
            redoc_url = None,
            openapi_url = None)

# Serve the openapi route for the docs page
@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(docs.get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

# Add all middleware
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins = origins, allow_credentials = True, allow_methods = ["*"], allow_headers = ["*"])
app.add_middleware(CatchExceptionsMiddleware) # This has to be on top of all other middleware except cors
app.add_middleware(ReqLogMiddleware)
app.add_middleware(DBMiddleware)

# Add all endpoint routers
app.include_router(auth.router) 
app.include_router(courses.router) 
app.include_router(docs.router) 
app.include_router(ml.router) 
app.include_router(mock.router)
app.include_router(professors.router) 
app.include_router(static.router) 
app.include_router(test.router) 
app.include_router(user.router) 
app.include_router(utils.router) 

# Load static webpages directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")