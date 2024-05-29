Welcome! This the git repository for the backend our FYP, HKUCompass

The folder structure is as follows:
app: A the directory housing the main app.
app/constants: Contains universal constants for the project.
app/data: Houses all code for the Data Collection Service.
app/data/courses_job: The job to collect all course information.
app/data/profs_job: The job to collect professor information.
app/db: Contains all code for the database connection.
app/db/schemas: Houses all schemas for all collections of the database.
app/logs: Houses all logging related code.
app/middleware: Houses all middlewares of the project.
app/mock_data: Contains mock_data for presentation purposes.
app/models: Contains all the hosted Machine Learning models code.
app/routes: All endpoints.
app/static: All static webpages served by the app.
app/utils: Houses some useful utility functions.
.env.sample: A sample file for how the .env file should look.
.gitignore: A file informing git about which file to ignore changes for.
.gitlab-ci.yml: The gitlab CI/CD script used to configure the build pipeline.
Dockerfile: The docker file used to build the project.
package.json: Contains some useful npm scripts for dev mode.
README.md: The current file you are reading.
requirements.txt: A text file with all the python requirements for the project.
setup.py: A python script to do some pre-processing if need be while buidling the project.

To run the project in dev mode, create a new .env file using the .env.sample file provided, then simply use the command `npm run dev` from the terminal