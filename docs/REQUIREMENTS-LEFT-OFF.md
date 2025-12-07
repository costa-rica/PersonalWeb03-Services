# Requirements LEFT-OFF.docx download and summary

## Overview

This service that automates the process of downloading a LEFT-OFF.docx file from OneDrive, extracting the most recent 7 days of activities, and generating an AI-powered summary using OpenAI. For creating this service I want to use the reference code in the `docs/reference-code` folder as a guide.

## Features

- Downloads LEFT-OFF.docx from OneDrive using Microsoft Graph API
- Parses the document to extract the most recent 7 days of activities
- Generates intelligent summaries using OpenAI's gpt-4o-mini model
- Comprehensive logging for tracking progress and debugging

## ENV

```
PATH_PROJECT_RESOURCES=/Users/nick/Documents/_project_resources/PersonalWeb03
NAME_TARGET_FILE = 'LEFT-OFF.docx'
TARGET_FILE_ID = SECRET_TARGET_FILE_ID
APPLICATION_ID=SECRET_APPLICATION_ID
CLIENT_SECRET=SECRET_CLIENT_SECRET
REFRESH_TOKEN=SECRET_REFRESH_TOKEN
URL_BASE_OPENAI=https://api.openai.com/v1
KEY_OPENAI=SECRET_KEY_OPENAI
```

## Steps
This service will be a three step process:

### Step 1: Download LEFT-OFF.docx file
- This process `docs/reference-code/onedrive_client.py`
- Uses Microsoft Graph API with MSAL (Microsoft Authentication Library)
- Authenticates via refresh token to obtain access tokens
- Downloads the target LEFT-OFF.docx file from OneDrive to the PATH_PROJECT_RESOURCES folder's sub folder called services-data
   - the file name is: `LEFT-OFF.docx`

### Step 2: Parse LEFT-OFF.docx file
- This process: `docs/reference-code/document_parser.py`
- Parses .docx files using python-docx library
- Extracts content from the last 7 days based on Heading 1 dates in YYYYMMDD format
- Converts document structure to markdown format
- Document structure expectation: Most recent entries at top, oldest at bottom
- Output file is found in the PATH_PROJECT_RESOURCES folder's sub folder called services-data
   - the file name is: `last-7-days-activities.md`

### Step 3: Generate AI-powered summary

- Uses OpenAI API (gpt-4o-mini by default)
- Reads a customizable prompt template from `src/templates/left-off-summarizer.md`
- Replaces the placeholder `<< last-7-days-activities.md >>` with extracted activities
- returns a JSON response with the summary and the datetime the summary was generated



