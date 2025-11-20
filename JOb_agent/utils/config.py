"""
Utility functions for loading API keys and configuration
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


def load_api_key(key_name: str) -> Optional[str]:
    """
    Load API key from environment variables
    
    Args:
        key_name: Name of the environment variable
        
    Returns:
        API key value or None if not found
    """
    api_key = os.getenv(key_name)
    if not api_key:
        print(f"Warning: {key_name} not found in environment variables")
        return None
    return api_key


def get_email_config() -> dict:
    """
    Get email configuration from environment variables
    
    Returns:
        Dictionary with email configuration
    """
    return {
        'email_address': os.getenv('EMAIL_ADDRESS'),
        'email_password': os.getenv('EMAIL_PASSWORD'),
        'imap_server': os.getenv('EMAIL_IMAP_SERVER', 'imap.gmail.com'),
        'imap_port': int(os.getenv('EMAIL_IMAP_PORT', '993')),
    }


def get_ai_config() -> dict:
    """
    Get AI model configuration from environment variables
    
    Returns:
        Dictionary with AI configuration
    """
    return {
        'model': os.getenv('AI_MODEL', 'gpt-4o-mini'),
        'temperature': float(os.getenv('TEMPERATURE', '0.3')),
        'openai_api_key': load_api_key('OPENAI_API_KEY'),
        'google_api_key': load_api_key('GOOGLE_API_KEY'),
    }


def get_monitoring_config() -> dict:
    """
    Get monitoring configuration from environment variables
    
    Returns:
        Dictionary with monitoring configuration
    """
    return {
        'check_interval': int(os.getenv('CHECK_INTERVAL', '3600')),
        'lookback_days': int(os.getenv('LOOKBACK_DAYS', '30')),
    }


def validate_config() -> bool:
    """
    Validate that all required configuration is present
    
    Returns:
        True if configuration is valid, False otherwise
    """
    email_config = get_email_config()
    ai_config = get_ai_config()
    
    required_fields = [
        ('EMAIL_ADDRESS', email_config['email_address']),
        ('EMAIL_PASSWORD', email_config['email_password']),
        ('OPENAI_API_KEY', ai_config['openai_api_key']),
    ]
    
    missing_fields = []
    for field_name, field_value in required_fields:
        if not field_value:
            missing_fields.append(field_name)
    
    if missing_fields:
        print(f"Error: Missing required configuration: {', '.join(missing_fields)}")
        print("Please check your .env file")
        return False
    
    return True


if __name__ == "__main__":
    # Test configuration
    print("Testing configuration...")
    if validate_config():
        print("✓ Configuration is valid!")
        print(f"Email: {get_email_config()['email_address']}")
        print(f"AI Model: {get_ai_config()['model']}")
        print(f"Check Interval: {get_monitoring_config()['check_interval']} seconds")
    else:
        print("✗ Configuration is invalid!")
