# 🔑 Configuration Guide - Required Parameters

## Overview
This guide explains **exactly** what you need to configure before testing your Job Agent, where to get each parameter, and how to add them.

---

## 📋 Required Parameters Checklist

### ✅ **REQUIRED** (Must have to run)
- [ ] `OPENAI_API_KEY` - For AI email classification
- [ ] `EMAIL_ADDRESS` - Your email address to monitor
- [ ] `EMAIL_PASSWORD` - Email account password/app password

### 🔶 **OPTIONAL** (Recommended but not required)
- [ ] `GOOGLE_API_KEY` - If you want to use Google's Gemini instead of OpenAI
- [ ] `EMAIL_IMAP_SERVER` - Auto-detected for Gmail/Outlook
- [ ] `EMAIL_IMAP_PORT` - Auto-detected (default: 993)
- [ ] `DATABASE_URL` - Custom database location
- [ ] `AI_MODEL` - Which AI model to use
- [ ] `CHECK_INTERVAL` - How often to check emails
- [ ] `LOOKBACK_DAYS` - How far back to scan initially

---

## 🔐 Step-by-Step Setup Guide

### Step 1: Create Your `.env` File

```bash
cd /Users/bharath/Documents/Git/AI_Agents/Multi_Agent/Ai_news_blog_agent/Agentic_AI/JOb_agent

# Copy the example file
cp .env.example .env

# Open it for editing
nano .env
# Or use your preferred editor: code .env, vim .env, etc.
```

---

### Step 2: Get Your OpenAI API Key

#### **What is it?**
API key that allows the Job Agent to use OpenAI's GPT models to classify and extract data from emails.

#### **How to get it:**

1. **Go to OpenAI Platform**
   - Visit: https://platform.openai.com/api-keys
   
2. **Sign in or Create Account**
   - Use your OpenAI account
   - If you don't have one, sign up at https://platform.openai.com/signup

3. **Create API Key**
   - Click "Create new secret key"
   - Give it a name like "Job Agent"
   - Copy the key (starts with `sk-proj-...` or `sk-...`)
   - ⚠️ **IMPORTANT**: Save it immediately! You can't see it again

4. **Set Up Billing** (if not already done)
   - Go to: https://platform.openai.com/account/billing
   - Add payment method
   - Add credits (minimum $5 recommended)
   - Note: Testing will cost approximately $0.10-0.50 depending on email volume

#### **How to add it:**
```bash
# In your .env file, replace:
OPENAI_API_KEY=your_openai_api_key_here

# With your actual key:
OPENAI_API_KEY=sk-proj-abc123xyz789...
```

#### **Cost Estimate:**
- Using `gpt-4o-mini` (recommended): ~$0.01 per 100 emails
- Using `gpt-4o`: ~$0.10 per 100 emails
- Using `gpt-4`: ~$0.50 per 100 emails

---

### Step 3: Configure Your Email Account

#### **What is it?**
Your email address and credentials so the agent can read your emails.

#### **Option A: Gmail (Recommended)**

##### **3A.1: Enable IMAP**
1. Go to Gmail Settings: https://mail.google.com/mail/u/0/#settings/fwdandpop
2. Click "Forwarding and POP/IMAP" tab
3. Under "IMAP access", select "Enable IMAP"
4. Click "Save Changes"

##### **3A.2: Create App Password** (REQUIRED for Gmail)
⚠️ **Do NOT use your regular Gmail password!**

1. **Enable 2-Step Verification** (if not already enabled)
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup process

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Job Agent" as the name
   - Click "Generate"
   - **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

3. **Add to .env file:**
```bash
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop  # Remove spaces from app password
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
```

#### **Option B: Outlook/Office 365**

1. **Enable IMAP** (usually enabled by default)
   - Go to Outlook Settings → Mail → Sync email
   - Ensure IMAP is enabled

2. **Create App Password** (if 2FA enabled)
   - Go to: https://account.microsoft.com/security
   - Click "Advanced security options"
   - Under "App passwords", create new password

3. **Add to .env file:**
```bash
EMAIL_ADDRESS=your.email@outlook.com
EMAIL_PASSWORD=your_password_or_app_password
EMAIL_IMAP_SERVER=outlook.office365.com
EMAIL_IMAP_PORT=993
```

#### **Option C: Yahoo Mail**

1. **Enable IMAP**
   - Go to Yahoo Mail Settings
   - Click "Security and Privacy"
   - Enable "Allow apps that use less secure sign in"

2. **Generate App Password**
   - Go to: https://login.yahoo.com/account/security
   - Click "Generate app password"
   - Select "Other App" and name it "Job Agent"
   - Copy the password

3. **Add to .env file:**
```bash
EMAIL_ADDRESS=your.email@yahoo.com
EMAIL_PASSWORD=your_app_password
EMAIL_IMAP_SERVER=imap.mail.yahoo.com
EMAIL_IMAP_PORT=993
```

#### **Option D: Other Email Providers**

For other providers, you need:
- IMAP server address (Google: "your_provider IMAP settings")
- IMAP port (usually 993 for SSL)
- Your email and password/app password

---

### Step 4: Optional - Google Gemini API (Alternative to OpenAI)

#### **What is it?**
Google's AI model as an alternative to OpenAI. You can use this instead of or alongside OpenAI.

#### **How to get it:**

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

#### **How to add it:**
```bash
GOOGLE_API_KEY=AIzaSy...your_key_here
```

#### **To use Gemini instead of OpenAI:**
```bash
AI_MODEL=gemini-pro
```

---

### Step 5: Configure Optional Settings

#### **Database Location**
```bash
# Default (recommended):
DATABASE_URL=sqlite:///job_tracker.db

# Custom location:
DATABASE_URL=sqlite:////absolute/path/to/your/database.db
```

#### **AI Model Selection**
```bash
# Recommended for testing (cheap and fast):
AI_MODEL=gpt-4o-mini

# Better quality but more expensive:
AI_MODEL=gpt-4o

# Best quality but most expensive:
AI_MODEL=gpt-4

# Google's model (requires GOOGLE_API_KEY):
AI_MODEL=gemini-pro
```

#### **Monitoring Settings**
```bash
# How often to check emails (in seconds)
CHECK_INTERVAL=3600  # 1 hour
# CHECK_INTERVAL=1800  # 30 minutes
# CHECK_INTERVAL=7200  # 2 hours

# How many days back to scan on first run
LOOKBACK_DAYS=30  # Last 30 days
# LOOKBACK_DAYS=7   # Last week
# LOOKBACK_DAYS=90  # Last 3 months
```

#### **AI Temperature (Creativity)**
```bash
# Lower = more consistent, Higher = more creative
TEMPERATURE=0.3  # Recommended for classification (0.0-1.0)
```

---

## 📝 Complete .env File Example

Here's a complete example with all parameters:

```bash
# ============================================
# REQUIRED PARAMETERS
# ============================================

# OpenAI API Key (REQUIRED)
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-abc123xyz789yourkey

# Email Configuration (REQUIRED)
# Your email address to monitor
EMAIL_ADDRESS=your.email@gmail.com

# For Gmail: Use App Password from https://myaccount.google.com/apppasswords
# For other providers: Your email password or app-specific password
EMAIL_PASSWORD=abcdefghijklmnop

# Email IMAP Server (auto-detected for Gmail/Outlook if not specified)
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993

# ============================================
# OPTIONAL PARAMETERS
# ============================================

# Google API Key (Optional - for Gemini models)
# Get from: https://makersuite.google.com/app/apikey
# GOOGLE_API_KEY=AIzaSy...your_key_here

# Database Configuration
DATABASE_URL=sqlite:///job_tracker.db

# Monitoring Settings
CHECK_INTERVAL=3600  # Check every hour (in seconds)
LOOKBACK_DAYS=30     # How many days back to check on first run

# AI Model Settings
AI_MODEL=gpt-4o-mini  # Options: gpt-4o-mini, gpt-4o, gpt-4, gemini-pro
TEMPERATURE=0.3       # 0.0 = consistent, 1.0 = creative

# ============================================
# ADVANCED SETTINGS (Usually don't need to change)
# ============================================

# Email folder to monitor (default: INBOX)
# EMAIL_FOLDER=INBOX

# Maximum emails to process per run (default: 100)
# MAX_EMAILS_PER_RUN=100

# Enable debug logging (default: false)
# DEBUG=true
```

---

## ✅ Verification Checklist

After configuring your `.env` file, verify:

### Required Parameters
- [ ] `OPENAI_API_KEY` starts with `sk-` and is complete
- [ ] `EMAIL_ADDRESS` is a valid email address
- [ ] `EMAIL_PASSWORD` is set (App Password for Gmail)
- [ ] No quotes around values (unless they contain spaces)
- [ ] No spaces around the `=` sign

### Email Configuration
- [ ] IMAP is enabled in your email account
- [ ] For Gmail: Using App Password, not regular password
- [ ] For Gmail: 2-Step Verification is enabled
- [ ] IMAP server and port are correct for your provider

### OpenAI Configuration
- [ ] API key is valid (test at platform.openai.com)
- [ ] Billing is set up
- [ ] You have credits available

---

## 🧪 Test Your Configuration

After setting up your `.env` file, test it:

```bash
# Test configuration validity
python -c "from utils.config import validate_config; print('✓ Valid!' if validate_config() else '✗ Invalid')"

# Test OpenAI connection
python -c "from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); print('✓ OpenAI connected!')"

# Test email connection (this will be done by the agent)
python test_agents.py
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` to Git**
   - It's already in `.gitignore`
   - Double-check before pushing code

2. **Use App Passwords**
   - Never use your main email password
   - Use provider-specific app passwords

3. **Rotate Keys Regularly**
   - Change API keys every few months
   - Regenerate app passwords periodically

4. **Limit API Key Permissions**
   - Use OpenAI's key permission settings
   - Set usage limits if available

5. **Keep Backups**
   - Save your `.env` file securely
   - Use a password manager for API keys

---

## 🆘 Troubleshooting

### "Configuration validation failed"
- Check that all required fields are filled
- Ensure no quotes around values
- Verify no extra spaces

### "OpenAI API error"
- Verify key is correct (starts with `sk-`)
- Check billing is set up
- Ensure you have credits

### "Email authentication failed"
- For Gmail: Use App Password, not regular password
- Verify IMAP is enabled
- Check email/password are correct
- Try removing spaces from app password

### "IMAP connection failed"
- Verify IMAP server address
- Check port is 993 (or 143 for non-SSL)
- Ensure firewall allows IMAP connections

---

## 📞 Quick Reference

| Provider | IMAP Server | Port | Notes |
|----------|-------------|------|-------|
| Gmail | `imap.gmail.com` | 993 | Requires App Password |
| Outlook | `outlook.office365.com` | 993 | May need App Password |
| Yahoo | `imap.mail.yahoo.com` | 993 | Requires App Password |
| iCloud | `imap.mail.me.com` | 993 | Requires App Password |

---

## 🎯 Next Steps

Once your `.env` file is configured:

1. **Verify configuration**: `python -c "from utils.config import validate_config; validate_config()"`
2. **Run tests**: `./quick_test.sh`
3. **Start testing**: `python main.py --mode once --days 1`

---

## 💡 Pro Tips

1. **Start with gpt-4o-mini** - It's cheap and works well for testing
2. **Use Gmail** - Easiest to set up with App Passwords
3. **Test with 1 day first** - `--days 1` to minimize API costs
4. **Keep your API keys safe** - Never share or commit them
5. **Monitor costs** - Check OpenAI usage dashboard regularly

---

Need help? Run the interactive setup script:
```bash
python setup_config.py
```
