# Job Agent Testing Guide

## Overview
This guide provides comprehensive testing strategies for the Job Application Email Tracker multi-agent system.

## Testing Levels

### 1. Unit Testing (Individual Agents)
Test each agent in isolation to ensure they perform their specific tasks correctly.

### 2. Integration Testing
Test how agents work together in the orchestration workflow.

### 3. End-to-End Testing
Test the complete workflow from email monitoring to database storage.

---

## Quick Start Testing

### Prerequisites
1. **Environment Setup**
   ```bash
   # Activate virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Verify installation
   pip list | grep agno
   ```

2. **Configuration**
   ```bash
   # Copy and configure .env file
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Database Initialization**
   ```bash
   python main.py --init-db
   ```

---

## Testing Methods

### Method 1: One-Time Scan (Recommended for Initial Testing)

This is the safest way to test without continuous monitoring:

```bash
# Test with recent emails from last 7 days
python main.py --mode once --days 7 --email-mode recent

# Test with unread emails only
python main.py --mode once --email-mode unread

# Test with all emails from last 30 days
python main.py --mode once --days 30 --email-mode all
```

**What to expect:**
- Agent initialization messages
- Email fetching progress
- Classification results
- Data extraction output
- Database storage confirmation

---

### Method 2: Unit Testing Individual Agents

Create a test script to test each agent separately:

```bash
# Run the unit test script
python test_agents.py
```

See `test_agents.py` for individual agent testing.

---

### Method 3: Dashboard Testing

View the results and analytics:

```bash
# Launch the Streamlit dashboard
python dashboard.py
```

**Dashboard Features:**
- View all tracked applications
- See statistics and charts
- Filter by status, company, date
- Export data

---

### Method 4: Scheduled Monitoring (Production Testing)

For ongoing monitoring:

```bash
# Check every hour (3600 seconds)
python main.py --mode scheduled --interval 3600

# Check every 30 minutes
python main.py --mode scheduled --interval 1800
```

**Note:** Press `Ctrl+C` to stop scheduled monitoring.

---

### Method 5: Continuous Monitoring

Real-time monitoring (advanced):

```bash
python main.py --mode continuous --interval 300
```

---

## Testing Checklist

### ✅ Pre-Test Checklist
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list`)
- [ ] `.env` file configured with valid credentials
- [ ] Database initialized (`python main.py --init-db`)
- [ ] Email credentials tested (can login to email manually)
- [ ] OpenAI API key valid (test at platform.openai.com)

### ✅ Functional Testing
- [ ] Email Monitor Agent connects successfully
- [ ] Emails are fetched without errors
- [ ] Classifier Agent identifies job-related emails
- [ ] Data Extractor Agent extracts company/role info
- [ ] Database Manager Agent stores data correctly
- [ ] Orchestrator Agent coordinates workflow properly

### ✅ Data Validation
- [ ] Check database for new entries: `sqlite3 job_tracker.db "SELECT * FROM applications;"`
- [ ] Verify extracted data accuracy
- [ ] Confirm status classifications are correct
- [ ] Check timestamps are accurate

### ✅ Error Handling
- [ ] Test with invalid email credentials
- [ ] Test with invalid API keys
- [ ] Test with empty inbox
- [ ] Test with non-job-related emails

---

## Debugging Tips

### 1. Check Logs
The system prints detailed logs. Look for:
- ✓ Success indicators
- ⚠️  Warnings
- ✗ Error messages

### 2. Verify Email Connection
```python
# Quick test script
from utils.config import load_config
config = load_config()
print(f"Email: {config.email_address}")
print(f"OpenAI Key: {config.openai_api_key[:10]}...")
```

### 3. Database Inspection
```bash
# View all applications
sqlite3 job_tracker.db "SELECT company_name, role_title, status FROM applications;"

# Count applications by status
sqlite3 job_tracker.db "SELECT status, COUNT(*) FROM applications GROUP BY status;"
```

### 4. Test Individual Components
```python
# Test email connection only
python -c "from agents.email_monitor_agent import create_email_monitor_agent; agent = create_email_monitor_agent(); print('Email agent created successfully!')"

# Test OpenAI connection
python -c "from openai import OpenAI; import os; client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); print('OpenAI connected!')"
```

---

## Common Issues & Solutions

### Issue 1: "Authentication failed"
**Solution:** 
- For Gmail: Use App Password, not regular password
- Enable IMAP in email settings
- Check 2FA settings

### Issue 2: "No emails found"
**Solution:**
- Increase `--days` parameter
- Use `--email-mode all`
- Check email folder (should be INBOX)

### Issue 3: "OpenAI API error"
**Solution:**
- Verify API key is valid
- Check API quota/billing
- Ensure key has proper permissions

### Issue 4: "Database locked"
**Solution:**
- Close any other programs accessing the database
- Delete `job_tracker.db` and reinitialize
- Check file permissions

---

## Performance Testing

### Metrics to Monitor
1. **Email Processing Speed**: Time to process each email
2. **Classification Accuracy**: % of correctly classified emails
3. **Extraction Accuracy**: Quality of extracted data
4. **API Usage**: Number of OpenAI API calls
5. **Database Performance**: Query response times

### Benchmarking
```bash
# Process 100 emails and measure time
time python main.py --mode once --days 90 --email-mode all
```

---

## Test Data

### Creating Test Emails
For thorough testing, send yourself test emails with:
1. Job application confirmations
2. Interview requests
3. Rejection emails
4. Job offers
5. General recruiter emails

### Sample Test Email Subjects
- "Thank you for your application to Software Engineer at Google"
- "Interview invitation - Senior Developer Role"
- "Update on your application"
- "We've decided to move forward with other candidates"
- "Job Offer - Product Manager Position"

---

## Automated Testing

### Running Pytest
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_email_classifier.py

# Run with coverage
pytest --cov=agents --cov-report=html
```

---

## Production Readiness Checklist

Before deploying to production:
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Error handling tested
- [ ] Logging configured properly
- [ ] Database backups configured
- [ ] API rate limiting handled
- [ ] Email credentials secured
- [ ] Monitoring/alerting set up
- [ ] Documentation complete
- [ ] Performance benchmarks met

---

## Next Steps

1. **Start Simple**: Begin with `--mode once` on a small date range
2. **Verify Results**: Check the dashboard and database
3. **Iterate**: Adjust parameters and test different scenarios
4. **Scale Up**: Move to scheduled monitoring once confident
5. **Monitor**: Keep an eye on logs and performance

---

## Support

If you encounter issues:
1. Check the logs for error messages
2. Review this testing guide
3. Consult the main README.md
4. Check individual agent files for documentation
5. Review the .env.example for configuration options
