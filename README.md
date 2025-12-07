# PersonalWeb03-Services

This repository contains the services for the PersonalWeb03 project. The goal of this project is to combine services that have needed for the PersonalWeb03 project into a single repository. These services are currently in separate repositories and the `docs/reference-code` folder will have some example code that should be used as a reference to build this project.

## Build requirements
This project will be a Python project that stores the codebase in the src/ folder. In production this will run on a a server that will run the services as a cron job. We want to set up the project so that by default `python src/main.py` will pass through a guardrail that will check for the time. 


### Guardrail specifications

The guardrail will check for the time and will prevent the execution of the service outside of the allowed window. The allowed window is defined as:
- **Allowed window**: Sunday 10:55 PM - 11:05 PM (local system time)
- **Buffer**: 5 minutes before and after 11:00 PM for clock synchronization tolerance
- **Exit behavior**: If run outside this window without the `--run-anyway` flag, the service logs a warning and exits with code 2
- **Bypass**: Use `--run-anyway` flag to run the service at any time for testing or manual execution

## Services
### 1. LEFT-OFF.docx download and summary
This service will download the LEFT-OFF.docx file from the MS Graph API and then summarize it using the OpenAI API.
- this specific function should be able to run at any time with the command `python src/main.py --run-left-off`

### 2. Toggl Tracker to CSV
This service will download the Toggl Tracker data from the Toggl API and then convert it to a CSV file.
- this specific function should be able to run at any time with the command `python src/main.py --run-toggl`



