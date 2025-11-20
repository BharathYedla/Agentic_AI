# Setup Guide for Job Application Email Tracker

## Prerequisites

- Python 3.8 or higher
- Gmail account (or other IMAP-compatible email service)
- OpenAI API key

## Step-by-Step Setup

### 1. Create Virtual Environment

```bash
cd JOb_agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Email Access

#### For Gmail Users:

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password

#### For Other Email Providers:

- **Outlook/Office365**: Use your regular password with IMAP enabled
- **Yahoo**: Generate an app password from account settings
- **Custom IMAP**: Use your IMAP server details

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your details:

```env
# API Keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# Email Configuration (Gmail example)
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your-16-char-app-password
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993

# For Outlook/Office365:
# EMAIL_IMAP_SERVER=outlook.office365.com
# EMAIL_IMAP_PORT=993

# For Yahoo:
# EMAIL_IMAP_SERVER=imap.mail.yahoo.com
# EMAIL_IMAP_PORT=993

# Database
DATABASE_URL=sqlite:///job_tracker.db

# Monitoring Settings
CHECK_INTERVAL=3600  # 1 hour
LOOKBACK_DAYS=30

# AI Model Settings
AI_MODEL=gpt-4o-mini  # or gpt-4, gpt-3.5-turbo
TEMPERATURE=0.3
```

### 5. Initialize Database

```bash
python main.py --init-db
```

### 6. Test Configuration

```bash
python -c "from utils.config import validate_config; validate_config()"
```

## Usage

### One-Time Scan

Scan recent emails once:

```bash
python main.py --mode once --days 7
```

### Continuous Monitoring

Monitor emails continuously (checks every hour):

```bash
python main.py --mode continuous --interval 3600
```

### Scheduled Monitoring

Run on a schedule (checks every 30 minutes):

```bash
python main.py --mode scheduled --interval 1800
```

### View Dashboard

Launch the web dashboard:

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at http://localhost:8501

## Command Line Options

```
--mode {once,continuous,scheduled}
    Monitoring mode (default: once)

--interval SECONDS
    Check interval for continuous/scheduled mode (default: 3600)

--days DAYS
    Number of days to look back (default: 7)

--email-mode {recent,unread,all}
    Email fetching mode (default: recent)

--init-db
    Initialize database and exit
```

## Troubleshooting

### Email Connection Issues

**Problem**: "Failed to connect to email server"

**Solutions**:
- Verify your email and password are correct
- For Gmail, ensure you're using an App Password, not your regular password
- Check if IMAP is enabled in your email settings
- Verify firewall isn't blocking port 993

### API Key Issues

**Problem**: "OpenAI API key not found"

**Solutions**:
- Ensure `.env` file exists in the project root
- Check that `OPENAI_API_KEY` is set correctly
- Verify no extra spaces or quotes around the key

### Database Issues

**Problem**: "Database error" or "Table not found"

**Solutions**:
```bash
# Reinitialize database
python main.py --init-db
```

### Import Errors

**Problem**: "ModuleNotFoundError"

**Solutions**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## Testing Individual Components

### Test Email Client

```bash
python utils/email_client.py
```

### Test Email Monitor Agent

```bash
python agents/email_monitor_agent.py
```

### Test Email Classifier Agent

```bash
python agents/email_classifier_agent.py
```

### Test Data Extractor Agent

```bash
python agents/data_extractor_agent.py
```

### Test Database Manager Agent

```bash
python agents/database_manager_agent.py
```

## Advanced Configuration

### Custom Email Filters

Edit `agents/email_monitor_agent.py` to customize job-related keywords:

```python
job_keywords = [
    'application', 'interview', 'position', 'opportunity',
    'recruiter', 'hiring', 'job', 'career', 'offer',
    # Add your custom keywords here
]
```

### Adjust AI Model Temperature

Lower temperature (0.1-0.3) = more consistent, deterministic
Higher temperature (0.5-0.9) = more creative, varied

Edit in `.env`:
```
TEMPERATURE=0.3
```

### Change AI Model

Available models:
- `gpt-4o-mini` (recommended, fast and cost-effective)
- `gpt-4o` (more capable, higher cost)
- `gpt-4` (most capable, highest cost)
- `gpt-3.5-turbo` (fast, lowest cost)

Edit in `.env`:
```
AI_MODEL=gpt-4o-mini
```

## Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use App Passwords** instead of your main email password
3. **Rotate API keys** periodically
4. **Limit API key permissions** if possible
5. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`

## Performance Tips

1. **Adjust check interval** based on your needs (longer = fewer API calls)
2. **Use `--email-mode unread`** to only process new emails
3. **Limit lookback days** to reduce processing time
4. **Monitor API usage** to stay within OpenAI rate limits

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the README.md
3. Check individual agent files for detailed documentation
