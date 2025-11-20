"""
Data Extractor Agent - Extracts structured information from job-related emails
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from utils.config import get_ai_config
from typing import Dict, Optional
import json
import re


def create_data_extractor_agent() -> Agent:
    """
    Create an agent that extracts data from emails
    
    Returns:
        Configured Agent instance
    """
    ai_config = get_ai_config()
    
    agent = Agent(
        name="Data Extractor Agent",
        role="Information Extraction Specialist",
        goal="Extract structured information from job-related emails with high accuracy",
        backstory="""You are an expert at extracting structured information from 
        unstructured text. You can identify company names, job titles, locations, 
        dates, and other relevant information from job-related emails.""",
        model=OpenAIChat(
            id=ai_config['model'],
            api_key=ai_config['openai_api_key'],
            temperature=0.1  # Lower temperature for more consistent extraction
        ),
        verbose=True,
        allow_delegation=False,
        markdown=True,
    )
    
    return agent


def extract_data_task(agent: Agent, email: Dict, classification: Dict) -> Dict:
    """
    Task to extract structured data from an email
    
    Args:
        agent: The data extractor agent
        email: Email dictionary
        classification: Classification result from classifier agent
        
    Returns:
        Extracted data dictionary
    """
    subject = email.get('subject', '')
    from_address = email.get('from', '')
    body = email.get('text', '') or email.get('body', '')
    email_date = email.get('date', '')
    
    # Truncate body if too long
    if len(body) > 3000:
        body = body[:3000] + "..."
    
    email_type = classification.get('classification', 'unknown')
    
    prompt = f"""
Extract structured information from this job-related email.

Email Type: {email_type}
Subject: {subject}
From: {from_address}
Date: {email_date}
Body: {body}

Extract the following information:
1. Company Name: The name of the company
2. Role/Position Title: The job title or position
3. Location: Job location (city, state, country, or "Remote")
4. Application Status: Current status (applied, rejected, interview_scheduled, offer_received, etc.)
5. Application Date: When you applied (if mentioned)
6. Salary Range: If mentioned
7. Job Description URL: Any links to job posting
8. Next Steps: Any action items or next steps mentioned
9. Interview Date/Time: If an interview is scheduled
10. Contact Person: Name of recruiter or contact person

Respond in JSON format:
{{
    "company_name": "string or null",
    "role_title": "string or null",
    "location": "string or null",
    "status": "string",
    "application_date": "YYYY-MM-DD or null",
    "salary_range": "string or null",
    "application_url": "string or null",
    "next_steps": "string or null",
    "interview_datetime": "YYYY-MM-DD HH:MM or null",
    "contact_person": "string or null",
    "additional_notes": "any other relevant information"
}}

Important:
- Use null for fields that cannot be determined
- For status, use one of: applied, rejected, interview_scheduled, offer_received, follow_up_needed
- Extract dates in YYYY-MM-DD format
- Be accurate and don't make assumptions
"""
    
    try:
        response = agent.run(prompt)
        response_text = str(response.content)
        
        # Extract JSON from markdown if present
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        elif '```' in response_text:
            json_start = response_text.find('```') + 3
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        
        extracted_data = json.loads(response_text)
        
        # Add email metadata
        extracted_data['email_subject'] = subject
        extracted_data['email_from'] = from_address
        extracted_data['email_date'] = email_date
        extracted_data['email_message_id'] = email.get('message_id')
        extracted_data['classification'] = email_type
        
        return extracted_data
        
    except Exception as e:
        print(f"✗ Error extracting data: {e}")
        # Return minimal data
        return {
            'company_name': extract_company_fallback(from_address, subject),
            'role_title': extract_role_fallback(subject),
            'location': None,
            'status': map_classification_to_status(email_type),
            'application_date': None,
            'salary_range': None,
            'application_url': None,
            'next_steps': None,
            'interview_datetime': None,
            'contact_person': None,
            'additional_notes': f'Extraction error: {str(e)}',
            'email_subject': subject,
            'email_from': from_address,
            'email_date': email_date,
            'email_message_id': email.get('message_id'),
            'classification': email_type,
        }


def extract_company_fallback(from_address: str, subject: str) -> Optional[str]:
    """Fallback method to extract company name from email address or subject"""
    # Try to extract from email domain
    if '@' in from_address:
        domain = from_address.split('@')[1]
        company = domain.split('.')[0]
        return company.title()
    return None


def extract_role_fallback(subject: str) -> Optional[str]:
    """Fallback method to extract role from subject line"""
    # Common patterns
    patterns = [
        r'(?:for|to|as)\s+(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Engineer|Developer|Manager|Analyst|Designer|Specialist)))',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Engineer|Developer|Manager|Analyst|Designer|Specialist))',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, subject)
        if match:
            return match.group(1)
    
    return None


def map_classification_to_status(classification: str) -> str:
    """Map email classification to application status"""
    status_map = {
        'application_confirmation': 'applied',
        'rejection': 'rejected',
        'interview_request': 'interview_scheduled',
        'offer': 'offer_received',
        'follow_up': 'follow_up_needed',
        'general': 'in_progress',
    }
    return status_map.get(classification, 'unknown')


def extract_data_batch(agent: Agent, emails: list, classifications: list) -> list:
    """
    Extract data from multiple emails
    
    Args:
        agent: The data extractor agent
        emails: List of email dictionaries
        classifications: List of classification results
        
    Returns:
        List of extracted data dictionaries
    """
    print(f"\n{'='*60}")
    print(f"📊 Data Extractor Agent: Extracting data from {len(emails)} emails")
    print(f"{'='*60}\n")
    
    results = []
    for i, (email, classification) in enumerate(zip(emails, classifications), 1):
        if classification.get('is_job_related', False):
            print(f"Extracting data {i}/{len(emails)}: {email.get('subject', 'No subject')[:50]}...")
            extracted = extract_data_task(agent, email, classification)
            results.append(extracted)
            print(f"  ✓ Extracted: {extracted.get('company_name', 'Unknown')} - {extracted.get('role_title', 'Unknown')}")
        else:
            print(f"Skipping {i}/{len(emails)}: Not job-related")
    
    print(f"\n✓ Data extraction complete: {len(results)} records extracted")
    return results


if __name__ == "__main__":
    # Test the data extractor agent
    agent = create_data_extractor_agent()
    print(f"Created agent: {agent.name}")
    
    # Test with a sample email
    test_email = {
        'message_id': 'test123',
        'subject': 'Interview Invitation - Senior Software Engineer at TechCorp',
        'from': 'recruiter@techcorp.com',
        'date': '2024-01-15',
        'body': '''Dear Candidate,

Thank you for your application to the Senior Software Engineer position at TechCorp.

We would like to invite you for an interview on January 20, 2024 at 2:00 PM.

The position is based in San Francisco, CA with a salary range of $150,000 - $180,000.

Please confirm your availability.

Best regards,
Jane Smith
Senior Recruiter
'''
    }
    
    test_classification = {
        'is_job_related': True,
        'classification': 'interview_request',
        'confidence': 0.95
    }
    
    result = extract_data_task(agent, test_email, test_classification)
    print(f"\nExtracted data:")
    print(json.dumps(result, indent=2))
