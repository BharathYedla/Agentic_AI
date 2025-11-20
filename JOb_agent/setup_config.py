#!/usr/bin/env python3
"""
Interactive Configuration Setup for Job Agent

This script helps you set up your .env file with all required parameters.
It will guide you through each step and validate your inputs.
"""

import os
import sys
from pathlib import Path
from getpass import getpass

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_step(number, text):
    """Print step number"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Step {number}: {text}{Colors.END}")

def get_input(prompt, default=None, required=True, password=False):
    """Get user input with optional default"""
    if default:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "
    
    if password:
        value = getpass(prompt_text)
    else:
        value = input(prompt_text).strip()
    
    if not value and default:
        return default
    
    if not value and required:
        print_error("This field is required!")
        return get_input(prompt, default, required, password)
    
    return value

def validate_email(email):
    """Basic email validation"""
    return '@' in email and '.' in email.split('@')[1]

def detect_imap_settings(email):
    """Auto-detect IMAP settings based on email domain"""
    domain = email.split('@')[1].lower()
    
    imap_settings = {
        'gmail.com': ('imap.gmail.com', 993),
        'googlemail.com': ('imap.gmail.com', 993),
        'outlook.com': ('outlook.office365.com', 993),
        'hotmail.com': ('outlook.office365.com', 993),
        'live.com': ('outlook.office365.com', 993),
        'yahoo.com': ('imap.mail.yahoo.com', 993),
        'icloud.com': ('imap.mail.me.com', 993),
        'me.com': ('imap.mail.me.com', 993),
    }
    
    return imap_settings.get(domain, (None, 993))

def test_openai_key(api_key):
    """Test if OpenAI API key is valid"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        # Try a minimal API call
        client.models.list()
        return True
    except Exception as e:
        print_error(f"OpenAI API key validation failed: {e}")
        return False

def main():
    """Main setup function"""
    print_header("Job Agent - Interactive Configuration Setup")
    
    print(f"{Colors.CYAN}This wizard will help you set up your .env file.{Colors.END}")
    print(f"{Colors.CYAN}You'll need:{Colors.END}")
    print("  • OpenAI API key")
    print("  • Email address and password/app password")
    print("\nPress Ctrl+C at any time to cancel.\n")
    
    input("Press Enter to continue...")
    
    config = {}
    
    # ===== STEP 1: OpenAI API Key =====
    print_step(1, "OpenAI API Key Configuration")
    print_info("You need an OpenAI API key to use GPT models for email classification.")
    print_info("Get your key from: https://platform.openai.com/api-keys")
    print_warning("Make sure you have billing set up and credits available!")
    print()
    
    while True:
        api_key = get_input("Enter your OpenAI API key", password=True, required=True)
        
        if not api_key.startswith('sk-'):
            print_error("OpenAI API keys should start with 'sk-'")
            retry = get_input("Try again? (y/n)", default="y", required=False)
            if retry.lower() != 'y':
                break
            continue
        
        print_info("Validating API key...")
        if test_openai_key(api_key):
            print_success("OpenAI API key is valid!")
            config['OPENAI_API_KEY'] = api_key
            break
        else:
            print_error("Could not validate API key. It might still work, but please verify.")
            use_anyway = get_input("Use this key anyway? (y/n)", default="n", required=False)
            if use_anyway.lower() == 'y':
                config['OPENAI_API_KEY'] = api_key
                break
    
    # ===== STEP 2: Email Configuration =====
    print_step(2, "Email Account Configuration")
    print_info("Configure the email account you want to monitor for job applications.")
    print()
    
    # Email address
    while True:
        email = get_input("Enter your email address", required=True)
        if validate_email(email):
            config['EMAIL_ADDRESS'] = email
            print_success(f"Email: {email}")
            break
        else:
            print_error("Invalid email address format")
    
    # Detect IMAP settings
    imap_server, imap_port = detect_imap_settings(email)
    
    if imap_server:
        print_success(f"Auto-detected IMAP server: {imap_server}:{imap_port}")
        config['EMAIL_IMAP_SERVER'] = imap_server
        config['EMAIL_IMAP_PORT'] = imap_port
        
        # Show provider-specific instructions
        domain = email.split('@')[1].lower()
        if 'gmail' in domain:
            print()
            print_warning("IMPORTANT: Gmail requires an App Password!")
            print_info("Steps to create Gmail App Password:")
            print("  1. Enable 2-Step Verification: https://myaccount.google.com/security")
            print("  2. Create App Password: https://myaccount.google.com/apppasswords")
            print("  3. Select 'Mail' and 'Other (Custom name)'")
            print("  4. Copy the 16-character password (remove spaces)")
            print()
        elif 'outlook' in domain or 'hotmail' in domain or 'live' in domain:
            print()
            print_info("For Outlook/Hotmail, you may need an App Password if 2FA is enabled")
            print_info("Create one at: https://account.microsoft.com/security")
            print()
    else:
        print_warning("Could not auto-detect IMAP settings for this provider")
        imap_server = get_input("Enter IMAP server address (e.g., imap.example.com)", required=True)
        imap_port = get_input("Enter IMAP port", default="993", required=True)
        config['EMAIL_IMAP_SERVER'] = imap_server
        config['EMAIL_IMAP_PORT'] = imap_port
    
    # Email password
    print()
    email_password = get_input("Enter your email password or App Password", password=True, required=True)
    config['EMAIL_PASSWORD'] = email_password
    print_success("Email password saved")
    
    # ===== STEP 3: Optional - Google API Key =====
    print_step(3, "Google Gemini API (Optional)")
    print_info("You can optionally add a Google API key to use Gemini models.")
    print_info("Get your key from: https://makersuite.google.com/app/apikey")
    print()
    
    add_google = get_input("Do you want to add a Google API key? (y/n)", default="n", required=False)
    if add_google.lower() == 'y':
        google_key = get_input("Enter your Google API key", password=True, required=False)
        if google_key:
            config['GOOGLE_API_KEY'] = google_key
            print_success("Google API key saved")
    
    # ===== STEP 4: AI Model Selection =====
    print_step(4, "AI Model Selection")
    print_info("Choose which AI model to use for email classification.")
    print()
    print("Available models:")
    print("  1. gpt-4o-mini    (Recommended - Fast and cheap, ~$0.01 per 100 emails)")
    print("  2. gpt-4o         (Better quality, ~$0.10 per 100 emails)")
    print("  3. gpt-4          (Best quality, ~$0.50 per 100 emails)")
    if 'GOOGLE_API_KEY' in config:
        print("  4. gemini-pro     (Google's model, requires Google API key)")
    print()
    
    model_choice = get_input("Select model (1-3)", default="1", required=False)
    model_map = {
        '1': 'gpt-4o-mini',
        '2': 'gpt-4o',
        '3': 'gpt-4',
        '4': 'gemini-pro'
    }
    config['AI_MODEL'] = model_map.get(model_choice, 'gpt-4o-mini')
    print_success(f"Selected model: {config['AI_MODEL']}")
    
    # ===== STEP 5: Monitoring Settings =====
    print_step(5, "Monitoring Settings")
    print_info("Configure how the agent monitors your emails.")
    print()
    
    # Check interval
    print("How often should the agent check for new emails? (in hours)")
    print("  1. Every 30 minutes")
    print("  2. Every hour (Recommended)")
    print("  3. Every 2 hours")
    print("  4. Every 4 hours")
    print()
    
    interval_choice = get_input("Select interval (1-4)", default="2", required=False)
    interval_map = {
        '1': 1800,   # 30 min
        '2': 3600,   # 1 hour
        '3': 7200,   # 2 hours
        '4': 14400   # 4 hours
    }
    config['CHECK_INTERVAL'] = interval_map.get(interval_choice, 3600)
    print_success(f"Check interval: {config['CHECK_INTERVAL']} seconds")
    
    # Lookback days
    print()
    lookback = get_input("How many days back to scan initially?", default="30", required=False)
    config['LOOKBACK_DAYS'] = lookback
    print_success(f"Will scan last {lookback} days on first run")
    
    # Temperature
    config['TEMPERATURE'] = '0.3'
    
    # Database URL
    config['DATABASE_URL'] = 'sqlite:///job_tracker.db'
    
    # ===== STEP 6: Write .env file =====
    print_step(6, "Saving Configuration")
    
    env_path = Path('.env')
    
    if env_path.exists():
        print_warning(".env file already exists!")
        overwrite = get_input("Overwrite existing .env file? (y/n)", default="n", required=False)
        if overwrite.lower() != 'y':
            print_info("Configuration not saved. Exiting.")
            return
        # Backup existing file
        backup_path = Path('.env.backup')
        env_path.rename(backup_path)
        print_success(f"Backed up existing .env to .env.backup")
    
    # Write .env file
    with open(env_path, 'w') as f:
        f.write("# Job Agent Configuration\n")
        f.write("# Generated by setup_config.py\n")
        f.write(f"# Created: {os.popen('date').read().strip()}\n\n")
        
        f.write("# ============================================\n")
        f.write("# REQUIRED PARAMETERS\n")
        f.write("# ============================================\n\n")
        
        f.write("# OpenAI API Key\n")
        f.write(f"OPENAI_API_KEY={config['OPENAI_API_KEY']}\n\n")
        
        f.write("# Email Configuration\n")
        f.write(f"EMAIL_ADDRESS={config['EMAIL_ADDRESS']}\n")
        f.write(f"EMAIL_PASSWORD={config['EMAIL_PASSWORD']}\n")
        f.write(f"EMAIL_IMAP_SERVER={config['EMAIL_IMAP_SERVER']}\n")
        f.write(f"EMAIL_IMAP_PORT={config['EMAIL_IMAP_PORT']}\n\n")
        
        if 'GOOGLE_API_KEY' in config:
            f.write("# ============================================\n")
            f.write("# OPTIONAL PARAMETERS\n")
            f.write("# ============================================\n\n")
            f.write("# Google API Key (Optional)\n")
            f.write(f"GOOGLE_API_KEY={config['GOOGLE_API_KEY']}\n\n")
        
        f.write("# Database\n")
        f.write(f"DATABASE_URL={config['DATABASE_URL']}\n\n")
        
        f.write("# Monitoring Settings\n")
        f.write(f"CHECK_INTERVAL={config['CHECK_INTERVAL']}\n")
        f.write(f"LOOKBACK_DAYS={config['LOOKBACK_DAYS']}\n\n")
        
        f.write("# AI Model Settings\n")
        f.write(f"AI_MODEL={config['AI_MODEL']}\n")
        f.write(f"TEMPERATURE={config['TEMPERATURE']}\n")
    
    print_success(".env file created successfully!")
    
    # ===== STEP 7: Summary =====
    print_header("Configuration Summary")
    
    print(f"{Colors.BOLD}Your configuration:{Colors.END}")
    print(f"  • Email: {config['EMAIL_ADDRESS']}")
    print(f"  • IMAP Server: {config['EMAIL_IMAP_SERVER']}:{config['EMAIL_IMAP_PORT']}")
    print(f"  • AI Model: {config['AI_MODEL']}")
    print(f"  • Check Interval: {config['CHECK_INTERVAL']} seconds")
    print(f"  • Lookback Days: {config['LOOKBACK_DAYS']}")
    print()
    
    print_success("Setup complete!")
    print()
    print(f"{Colors.CYAN}{Colors.BOLD}Next steps:{Colors.END}")
    print("  1. Test your configuration:")
    print(f"     {Colors.BLUE}python -c \"from utils.config import validate_config; validate_config()\"{Colors.END}")
    print()
    print("  2. Run the test suite:")
    print(f"     {Colors.BLUE}./quick_test.sh{Colors.END}")
    print()
    print("  3. Start testing with real emails:")
    print(f"     {Colors.BLUE}python main.py --mode once --days 1{Colors.END}")
    print()
    print("  4. View results in dashboard:")
    print(f"     {Colors.BLUE}python dashboard.py{Colors.END}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
