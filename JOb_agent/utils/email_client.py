"""
Email client for connecting to IMAP servers and fetching emails
"""
from imap_tools import MailBox, AND
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from utils.config import get_email_config
import email
from email.header import decode_header


class EmailClient:
    """Client for connecting to email servers and fetching emails"""
    
    def __init__(self):
        """Initialize email client with configuration"""
        self.config = get_email_config()
        self.mailbox = None
        
    def connect(self) -> bool:
        """
        Connect to the email server
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.mailbox = MailBox(self.config['imap_server'])
            self.mailbox.login(
                self.config['email_address'],
                self.config['email_password']
            )
            print(f"✓ Connected to {self.config['imap_server']}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to email server: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the email server"""
        if self.mailbox:
            self.mailbox.logout()
            print("✓ Disconnected from email server")
    
    def fetch_recent_emails(self, days: int = 7, folder: str = 'INBOX') -> List[Dict]:
        """
        Fetch recent emails from the specified folder
        
        Args:
            days: Number of days to look back
            folder: Email folder to search (default: INBOX)
            
        Returns:
            List of email dictionaries
        """
        if not self.mailbox:
            print("Error: Not connected to email server")
            return []
        
        try:
            # Calculate date range
            since_date = datetime.now() - timedelta(days=days)
            
            # Fetch emails
            emails = []
            for msg in self.mailbox.fetch(
                AND(date_gte=since_date.date()),
                mark_seen=False
            ):
                email_data = {
                    'message_id': msg.uid,
                    'subject': msg.subject,
                    'from': msg.from_,
                    'to': msg.to,
                    'date': msg.date,
                    'body': msg.text or msg.html,
                    'html': msg.html,
                    'text': msg.text,
                }
                emails.append(email_data)
            
            print(f"✓ Fetched {len(emails)} emails from last {days} days")
            return emails
            
        except Exception as e:
            print(f"✗ Error fetching emails: {e}")
            return []
    
    def fetch_unread_emails(self, folder: str = 'INBOX') -> List[Dict]:
        """
        Fetch unread emails from the specified folder
        
        Args:
            folder: Email folder to search (default: INBOX)
            
        Returns:
            List of email dictionaries
        """
        if not self.mailbox:
            print("Error: Not connected to email server")
            return []
        
        try:
            emails = []
            for msg in self.mailbox.fetch(AND(seen=False), mark_seen=False):
                email_data = {
                    'message_id': msg.uid,
                    'subject': msg.subject,
                    'from': msg.from_,
                    'to': msg.to,
                    'date': msg.date,
                    'body': msg.text or msg.html,
                    'html': msg.html,
                    'text': msg.text,
                }
                emails.append(email_data)
            
            print(f"✓ Fetched {len(emails)} unread emails")
            return emails
            
        except Exception as e:
            print(f"✗ Error fetching unread emails: {e}")
            return []
    
    def search_emails(self, query: str, days: int = 30) -> List[Dict]:
        """
        Search emails by subject or body
        
        Args:
            query: Search query
            days: Number of days to look back
            
        Returns:
            List of matching email dictionaries
        """
        if not self.mailbox:
            print("Error: Not connected to email server")
            return []
        
        try:
            since_date = datetime.now() - timedelta(days=days)
            emails = []
            
            for msg in self.mailbox.fetch(
                AND(date_gte=since_date.date()),
                mark_seen=False
            ):
                # Simple search in subject and body
                if (query.lower() in msg.subject.lower() or 
                    query.lower() in (msg.text or '').lower()):
                    email_data = {
                        'message_id': msg.uid,
                        'subject': msg.subject,
                        'from': msg.from_,
                        'to': msg.to,
                        'date': msg.date,
                        'body': msg.text or msg.html,
                        'html': msg.html,
                        'text': msg.text,
                    }
                    emails.append(email_data)
            
            print(f"✓ Found {len(emails)} emails matching '{query}'")
            return emails
            
        except Exception as e:
            print(f"✗ Error searching emails: {e}")
            return []


if __name__ == "__main__":
    # Test email client
    client = EmailClient()
    if client.connect():
        emails = client.fetch_recent_emails(days=7)
        print(f"\nRecent emails: {len(emails)}")
        if emails:
            print(f"\nFirst email:")
            print(f"  Subject: {emails[0]['subject']}")
            print(f"  From: {emails[0]['from']}")
            print(f"  Date: {emails[0]['date']}")
        client.disconnect()
