# Job Application Email Tracker

A multi-agent AI system that automatically tracks and analyzes job application emails, maintaining a comprehensive data room of all your job applications.

## Features

- 🔍 **Automatic Email Monitoring**: Real-time or scheduled monitoring of your inbox
- 🤖 **Intelligent Classification**: AI-powered classification of job-related emails
- 📊 **Data Extraction**: Automatically extracts company details, role, and application status
- 💾 **Persistent Storage**: SQLite database for tracking all applications
- 📈 **Analytics Dashboard**: View statistics and insights about your job search
- 🔔 **Notifications**: Get notified about important updates

## Architecture

### Multi-Agent System

1. **Email Monitor Agent**: Connects to your email provider and fetches new emails
2. **Email Classifier Agent**: Determines if an email is job-related and its type
3. **Data Extractor Agent**: Extracts structured information from emails
4. **Database Manager Agent**: Handles all database operations
5. **Orchestrator Agent**: Coordinates the workflow between all agents

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`
2. Add your API keys and email credentials:
   ```
   OPENAI_API_KEY=your_openai_key
   GOOGLE_API_KEY=your_google_key  # Optional
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```

## Usage

### One-time Scan
```bash
python main.py --mode once
```

### Scheduled Monitoring (every hour)
```bash
python main.py --mode scheduled --interval 3600
```

### Continuous Monitoring
```bash
python main.py --mode continuous
```

### View Dashboard
```bash
python dashboard.py
```

## Database Schema

The system maintains a SQLite database with the following structure:

- **applications**: Stores all job applications
  - company_name
  - role_title
  - status (applied, rejected, interview, offer, etc.)
  - application_date
  - last_updated
  - email_subject
  - email_body
  - metadata (JSON)

## Email Classification Types

- **Application Confirmation**: Automated confirmations of application receipt
- **Rejection**: Rejection emails
- **Interview Request**: Interview invitations
- **Offer**: Job offers
- **Follow-up**: Follow-up emails from recruiters
- **General**: Other job-related communications

## Supported Email Providers

- Gmail (via IMAP)
- Outlook/Office365
- Yahoo Mail
- Any IMAP-compatible email service

## License

MIT License
