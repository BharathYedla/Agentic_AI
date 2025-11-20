# 🎯 Quick Reference Card - Configuration Parameters

## 📋 Required Parameters (Must Have)

### 1. OPENAI_API_KEY
```bash
OPENAI_API_KEY=sk-proj-abc123xyz789...
```
- **What**: API key for OpenAI GPT models
- **Where to get**: https://platform.openai.com/api-keys
- **Cost**: ~$0.01 per 100 emails (gpt-4o-mini)
- **Setup**: 
  1. Sign up/login to OpenAI
  2. Go to API keys section
  3. Create new key
  4. Add billing ($5 minimum recommended)

### 2. EMAIL_ADDRESS
```bash
EMAIL_ADDRESS=your.email@gmail.com
```
- **What**: Your email address to monitor
- **Format**: Standard email format
- **Example**: `john.doe@gmail.com`

### 3. EMAIL_PASSWORD
```bash
EMAIL_PASSWORD=abcdefghijklmnop
```
- **What**: Password or App Password for email
- **Gmail**: MUST use App Password (not regular password)
  - Get from: https://myaccount.google.com/apppasswords
  - Requires 2-Step Verification enabled
- **Outlook**: App Password if 2FA enabled
- **Yahoo**: App Password required

---

## 🔶 Optional Parameters (Recommended)

### 4. EMAIL_IMAP_SERVER
```bash
EMAIL_IMAP_SERVER=imap.gmail.com
```
- **What**: IMAP server address
- **Auto-detected for**: Gmail, Outlook, Yahoo
- **Common values**:
  - Gmail: `imap.gmail.com`
  - Outlook: `outlook.office365.com`
  - Yahoo: `imap.mail.yahoo.com`

### 5. EMAIL_IMAP_PORT
```bash
EMAIL_IMAP_PORT=993
```
- **What**: IMAP port number
- **Default**: 993 (SSL/TLS)
- **Rarely needs changing**

### 6. AI_MODEL
```bash
AI_MODEL=gpt-4o-mini
```
- **What**: Which AI model to use
- **Options**:
  - `gpt-4o-mini` - Recommended (cheap, fast)
  - `gpt-4o` - Better quality
  - `gpt-4` - Best quality (expensive)
  - `gemini-pro` - Google's model

### 7. CHECK_INTERVAL
```bash
CHECK_INTERVAL=3600
```
- **What**: How often to check emails (seconds)
- **Common values**:
  - `1800` - Every 30 minutes
  - `3600` - Every hour (recommended)
  - `7200` - Every 2 hours

### 8. LOOKBACK_DAYS
```bash
LOOKBACK_DAYS=30
```
- **What**: How many days back to scan initially
- **Recommended**: 30 days
- **Range**: 1-90 days

---

## 📝 Complete Example .env File

```bash
# REQUIRED
OPENAI_API_KEY=sk-proj-abc123xyz789yourkey
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop

# OPTIONAL (but recommended)
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
DATABASE_URL=sqlite:///job_tracker.db
CHECK_INTERVAL=3600
LOOKBACK_DAYS=30
AI_MODEL=gpt-4o-mini
TEMPERATURE=0.3
```

---

## 🚀 Quick Setup Methods

### Method 1: Interactive Setup (Easiest)
```bash
python setup_config.py
```
Guides you through each parameter with validation.

### Method 2: Manual Setup
```bash
# Copy example file
cp .env.example .env

# Edit with your favorite editor
nano .env
# or
code .env
# or
vim .env
```

### Method 3: Command Line
```bash
cat > .env << 'EOF'
OPENAI_API_KEY=your_key_here
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
DATABASE_URL=sqlite:///job_tracker.db
CHECK_INTERVAL=3600
LOOKBACK_DAYS=30
AI_MODEL=gpt-4o-mini
TEMPERATURE=0.3
EOF
```

---

## ✅ Verification Commands

```bash
# Check if .env exists
ls -la .env

# Validate configuration
python -c "from utils.config import validate_config; validate_config()"

# Test OpenAI connection
python -c "from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); print('✓ Connected!')"

# Run full test suite
./quick_test.sh
```

---

## 🔑 Where to Get Each Key

| Parameter | URL | Notes |
|-----------|-----|-------|
| OpenAI API Key | https://platform.openai.com/api-keys | Requires billing setup |
| Gmail App Password | https://myaccount.google.com/apppasswords | Requires 2FA enabled |
| Outlook App Password | https://account.microsoft.com/security | If 2FA enabled |
| Google API Key | https://makersuite.google.com/app/apikey | Optional, for Gemini |

---

## 💰 Cost Estimates

| Model | Cost per 100 emails | Recommended for |
|-------|---------------------|-----------------|
| gpt-4o-mini | ~$0.01 | Testing & Production |
| gpt-4o | ~$0.10 | Better accuracy needed |
| gpt-4 | ~$0.50 | Best quality needed |
| gemini-pro | Free tier available | Alternative to OpenAI |

---

## 🆘 Common Issues

### "Configuration validation failed"
→ Check all required fields are filled
→ Remove quotes around values
→ No spaces around `=` sign

### "OpenAI API error"
→ Verify key starts with `sk-`
→ Check billing is set up
→ Ensure credits available

### "Email authentication failed"
→ Gmail: Use App Password, not regular password
→ Enable IMAP in email settings
→ Remove spaces from app password

---

## 📞 Quick Help

**Need help?** Read the full guide:
```bash
cat CONFIGURATION_GUIDE.md
```

**Interactive setup:**
```bash
python setup_config.py
```

**Test configuration:**
```bash
./quick_test.sh
```
