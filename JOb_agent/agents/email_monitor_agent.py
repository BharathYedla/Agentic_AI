"""
Email Monitor Agent - Monitors and fetches emails from inbox
"""
from agno.agent import Agent
from utils.email_client import EmailClient
from typing import List, Dict


def create_email_monitor_agent() -> Agent:
    """
    Create an agent that monitors and fetches emails
    
    Returns:
        Configured Agent instance
    """
    agent = Agent(
        name="Email Monitor Agent",
        role="Email Monitoring Specialist",
        description="Monitor email inbox and fetch job-related emails efficiently",
        instructions="""You are an expert at monitoring email inboxes and identifying 
        relevant emails. You work efficiently to fetch emails without missing any 
        important messages.""",
        debug_mode=True,
    )
    
    return agent


def fetch_emails_task(agent: Agent, days: int = 7, mode: str = 'recent') -> List[Dict]:
    """
    Task to fetch emails from inbox
    
    Args:
        agent: The email monitor agent
        days: Number of days to look back (for 'recent' mode)
        mode: 'recent', 'unread', or 'all'
        
    Returns:
        List of email dictionaries
    """
    print(f"\n{'='*60}")
    print(f"📧 Email Monitor Agent: Fetching emails (mode: {mode})")
    print(f"{'='*60}\n")
    
    client = EmailClient()
    
    try:
        if not client.connect():
            print("Failed to connect to email server")
            return []
        
        if mode == 'unread':
            emails = client.fetch_unread_emails()
        elif mode == 'recent':
            emails = client.fetch_recent_emails(days=days)
        else:
            emails = client.fetch_recent_emails(days=days)
        
        print(f"\n✓ Successfully fetched {len(emails)} emails")
        return emails
        
    except Exception as e:
        print(f"✗ Error in email monitoring: {e}")
        return []
        
    finally:
        client.disconnect()


def search_job_emails_task(agent: Agent, days: int = 30) -> List[Dict]:
    """
    Task to search for job-related emails using keywords
    
    Args:
        agent: The email monitor agent
        days: Number of days to look back
        
    Returns:
        List of job-related email dictionaries
    """
    print(f"\n{'='*60}")
    print(f"🔍 Email Monitor Agent: Searching for job-related emails")
    print(f"{'='*60}\n")
    
    # Common job-related keywords
    job_keywords = [
        'application', 'interview', 'position', 'opportunity',
        'recruiter', 'hiring', 'job', 'career', 'offer'
    ]
    
    client = EmailClient()
    all_job_emails = []
    
    try:
        if not client.connect():
            print("Failed to connect to email server")
            return []
        
        # Search for each keyword
        for keyword in job_keywords:
            emails = client.search_emails(keyword, days=days)
            all_job_emails.extend(emails)
        
        # Remove duplicates based on message_id
        unique_emails = {email['message_id']: email for email in all_job_emails}
        unique_job_emails = list(unique_emails.values())
        
        print(f"\n✓ Found {len(unique_job_emails)} unique job-related emails")
        return unique_job_emails
        
    except Exception as e:
        print(f"✗ Error searching for job emails: {e}")
        return []
        
    finally:
        client.disconnect()


if __name__ == "__main__":
    # Test the email monitor agent
    agent = create_email_monitor_agent()
    print(f"Created agent: {agent.name}")
    
    # Test fetching recent emails
    emails = fetch_emails_task(agent, days=7, mode='recent')
    print(f"\nFetched {len(emails)} emails")
    
    if emails:
        print("\nSample email:")
        print(f"  Subject: {emails[0]['subject']}")
        print(f"  From: {emails[0]['from']}")
