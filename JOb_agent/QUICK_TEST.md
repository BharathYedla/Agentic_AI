# 🧪 How to Test Your Job Agent - Quick Start Guide

## ✅ Prerequisites Checklist

Before testing, make sure you have:
- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with your credentials
- [ ] OpenAI API key (required)
- [ ] Email credentials (Gmail App Password recommended)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Setup Environment
```bash
cd /Users/bharath/Documents/Git/AI_Agents/Multi_Agent/Ai_news_blog_agent/Agentic_AI/JOb_agent

# Activate virtual environment
source venv/bin/activate

# Configure your .env file (if not already done)
cp .env.example .env
# Edit .env with your credentials
```

### Step 2: Run Quick Test
```bash
# This will test all components automatically
./quick_test.sh
```

**What this does:**
- ✓ Checks virtual environment
- ✓ Verifies dependencies
- ✓ Initializes database
- ✓ Tests all agents individually
- ✓ Shows detailed results

---

## 📋 Testing Methods

### Method 1: Automated Unit Testing (Recommended First)
```bash
python test_agents.py
```

**Tests performed:**
1. Configuration validation
2. Database initialization
3. Email Monitor Agent
4. Email Classifier Agent
5. Data Extractor Agent
6. Database Manager Agent
7. Orchestrator Agent

**Expected output:** Beautiful table showing pass/fail for each test

---

### Method 2: One-Time Email Scan (Real Test)
```bash
# Scan last 7 days of emails
python main.py --mode once --days 7 --email-mode recent

# Scan only unread emails
python main.py --mode once --email-mode unread

# Scan all emails from last 30 days
python main.py --mode once --days 30 --email-mode all
```

**What happens:**
1. Connects to your email account
2. Fetches emails based on your criteria
3. Classifies each email (job-related or not)
4. Extracts company, role, status information
5. Stores results in database
6. Shows summary of processed emails

---

### Method 3: View Dashboard
```bash
python dashboard.py
```

**Dashboard features:**
- View all tracked applications
- See statistics (total, by status, by company)
- Filter and search applications
- View timeline of applications
- Export data

---

### Method 4: Test with Sample Emails
```bash
# Generate sample test emails
python sample_test_emails.py
```

**This creates:**
- Sample job application emails
- Interview invitations
- Rejection emails
- Job offers
- Follow-up emails

**Then:**
1. Send these to yourself
2. Run: `python main.py --mode once --days 1`
3. Verify correct classification

---

## 🔍 Detailed Testing Workflow

### Phase 1: Environment Validation
```bash
# Check Python version
python --version  # Should be 3.11+

# Check if in virtual environment
echo $VIRTUAL_ENV  # Should show path to venv

# Verify dependencies
pip list | grep -E "agno|openai|imap-tools"
```

### Phase 2: Configuration Test
```bash
# Test configuration
python -c "from utils.config import validate_config; print('Valid!' if validate_config() else 'Invalid!')"
```

### Phase 3: Database Test
```bash
# Initialize database
python main.py --init-db

# Verify database created
ls -lh job_tracker.db

# Check database contents
sqlite3 job_tracker.db "SELECT COUNT(*) FROM applications;"
```

### Phase 4: Agent Testing
```bash
# Run comprehensive agent tests
python test_agents.py
```

### Phase 5: End-to-End Test
```bash
# Run full workflow
python main.py --mode once --days 7
```

### Phase 6: Results Verification
```bash
# View in dashboard
python dashboard.py

# Or check database directly
sqlite3 job_tracker.db "SELECT company_name, role_title, status FROM applications ORDER BY application_date DESC LIMIT 10;"
```

---

## 📊 Understanding Test Results

### Successful Test Output
```
✓ Configuration valid
✓ Database ready
✓ Email Monitor Agent created
✓ Fetched 15 emails
✓ Classified 8 as job-related
✓ Extracted data from 8 emails
✓ Stored 8 applications in database
```

### Common Issues

#### Issue: "Authentication failed"
**Solution:**
- For Gmail: Use App Password (Settings → Security → 2-Step Verification → App Passwords)
- Enable IMAP in Gmail settings
- Check email/password in `.env`

#### Issue: "OpenAI API error"
**Solution:**
- Verify API key at platform.openai.com
- Check billing/quota
- Ensure key is in `.env` file

#### Issue: "No emails found"
**Solution:**
- Increase `--days` parameter
- Use `--email-mode all`
- Check if you have job-related emails in inbox

#### Issue: "Database locked"
**Solution:**
- Close dashboard if running
- Delete `job_tracker.db` and reinitialize
- Check file permissions

---

## 🎯 Testing Checklist

### Basic Functionality
- [ ] Configuration loads correctly
- [ ] Database initializes without errors
- [ ] Email connection successful
- [ ] Emails are fetched
- [ ] Job emails are classified correctly
- [ ] Data extraction works
- [ ] Data is stored in database
- [ ] Dashboard displays data

### Advanced Testing
- [ ] Handles non-job emails correctly (ignores them)
- [ ] Correctly identifies different email types (rejection, offer, interview)
- [ ] Extracts company names accurately
- [ ] Extracts role titles accurately
- [ ] Sets correct status (applied, interview, rejected, offer)
- [ ] Handles duplicate emails
- [ ] Works with different email providers

### Performance Testing
- [ ] Processes emails in reasonable time
- [ ] Doesn't exceed API rate limits
- [ ] Database queries are fast
- [ ] Memory usage is acceptable

---

## 📈 Next Steps After Testing

### If All Tests Pass ✅
1. **Start with one-time scans** to build your initial database
2. **Review results** in the dashboard
3. **Set up scheduled monitoring** for ongoing tracking
4. **Customize** email filters and classification rules if needed

```bash
# Start scheduled monitoring (checks every hour)
python main.py --mode scheduled --interval 3600
```

### If Tests Fail ❌
1. **Check error messages** carefully
2. **Review TESTING_GUIDE.md** for troubleshooting
3. **Verify .env configuration**
4. **Test individual components** with `test_agents.py`
5. **Check logs** for detailed error information

---

## 🛠️ Useful Commands

```bash
# Quick test everything
./quick_test.sh

# Test individual agents
python test_agents.py

# One-time scan
python main.py --mode once

# View dashboard
python dashboard.py

# Check database
sqlite3 job_tracker.db "SELECT * FROM applications;"

# Reset database
rm job_tracker.db && python main.py --init-db

# View sample emails
python sample_test_emails.py

# Monitor logs in real-time
python main.py --mode once --days 1 2>&1 | tee test.log
```

---

## 📚 Additional Resources

- **TESTING_GUIDE.md** - Comprehensive testing documentation
- **README.md** - Project overview and features
- **SETUP.md** - Detailed setup instructions
- **.env.example** - Configuration template

---

## 💡 Pro Tips

1. **Start Small**: Test with `--days 1` first, then increase
2. **Use Sample Emails**: Generate and send test emails to yourself
3. **Check Dashboard**: Always verify results visually
4. **Monitor API Usage**: Keep an eye on OpenAI API costs
5. **Backup Database**: Copy `job_tracker.db` before major changes
6. **Test Regularly**: Run `test_agents.py` after any code changes

---

## 🎉 Success Criteria

Your Job Agent is working correctly if:
- ✅ All unit tests pass
- ✅ Emails are fetched successfully
- ✅ Job-related emails are identified (>80% accuracy)
- ✅ Company names and roles are extracted correctly
- ✅ Data appears in dashboard
- ✅ No critical errors in logs

---

## 🆘 Getting Help

If you encounter issues:
1. Check the error message carefully
2. Review TESTING_GUIDE.md troubleshooting section
3. Verify your .env configuration
4. Test with sample emails first
5. Check individual agents with test_agents.py

---

**Ready to test? Run this command:**
```bash
./quick_test.sh
```

Good luck! 🚀
