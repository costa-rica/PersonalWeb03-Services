![PersonalWeb03 Logo](docs/assets/personalWeb03Logo.png)

# PersonalWeb03-Services

Automated services for PersonalWeb03 that run as scheduled cron jobs on Sunday evenings. Downloads and processes data from OneDrive and Toggl Track APIs.

## Outputs

### LEFT-OFF Service

**File**: `services-data/left-off-7-day-summary.json`

Generates AI-powered summaries of the last 7 days of activities from LEFT-OFF.docx.

```json
{
  "summary": "- Continued work on CadmusAI, focusing on IP address rate limiting.\n- Presented at the MLH / DigitalOcean Hackathon, deployed live demo.\n- Made UI fixes and architectural changes to PersonalWeb03.\n- Restored old blog entries and added admin features.",
  "datetime_summary": "2025-12-07 12:00:00"
}
```

**Temp Files**: `services-data/left-off-temp/`
- `LEFT-OFF.docx` - Downloaded document from OneDrive
- `last-7-days-activities.md` - Extracted activities in markdown

---

### Toggl Service

**File**: `services-data/project_time_entries.csv`

Tracks time worked on each project over the last 7 days.

```csv
project_name,hours_worked,datetime_collected
Sharpening the Saw,31.68,2025-12-07 12:18:50
Networking - DataKind,10.49,2025-12-07 12:18:50
Search for work,3.21,2025-12-07 12:18:50
```

---

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

**Environment Variables**: Add to `.env`
```bash
# Shared
PATH_PROJECT_RESOURCES=/path/to/project/resources

# LEFT-OFF Service
TARGET_FILE_ID=your_onedrive_file_id
APPLICATION_ID=your_azure_app_id
CLIENT_SECRET=your_azure_client_secret
REFRESH_TOKEN=your_refresh_token
KEY_OPENAI=your_openai_api_key

# Toggl Service
TOGGL_API_TOKEN=your_toggl_api_token
```

---

## Usage

```bash
# Run individual services (anytime)
python src/main.py --run-left-off
python src/main.py --run-toggl

# Check time guardrail (scheduled execution)
python src/main.py                    # Exits with code 2 if outside Sunday 10:55-11:05 PM window
python src/main.py --run-anyway       # Bypass time restrictions
```

**Exit Codes**:
- `0` - Success
- `1` - Error (auth, API, file issues)
- `2` - Time restriction (outside allowed window)

---

## Documentation

- **[DEVELOPMENT_NOTES.md](docs/DEVELOPMENT_NOTES.md)** - Complete engineering reference with API details, architecture, and troubleshooting
- **requirements/** - Original specifications used for initial development (historical reference)

---

## Time-Based Guardrail

Services are designed to run as Sunday evening cron jobs:
- **Allowed Window**: Sunday 10:55 PM - 11:05 PM (local system time)
- **Bypass**: Use `--run-anyway` flag for testing
- Individual service flags (`--run-left-off`, `--run-toggl`) always bypass the guardrail
