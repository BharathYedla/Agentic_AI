"""
Email Classifier Agent - Classifies emails as job-related and determines their type
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from utils.config import get_ai_config
from typing import Dict, Optional
import json


def create_email_classifier_agent() -> Agent:
    """
    Create an agent that classifies emails
    
    Returns:
        Configured Agent instance
    """
    ai_config = get_ai_config()
    
    agent = Agent(
        name="Email Classifier Agent",
        role="Email Classification Specialist",
        description="Accurately classify emails as job-related and determine their type",
        instructions="""You are an expert at analyzing emails and determining if they 
        are related to job applications. You can identify application confirmations, 
        rejections, interview requests, offers, and other job-related communications 
        with high accuracy.""",
        model=OpenAIChat(
            id=ai_config['model'],
            api_key=ai_config['openai_api_key'],
            temperature=ai_config['temperature']
        ),
        debug_mode=True,
        markdown=True,
    )
    
    return agent


def classify_email_task(agent: Agent, email: Dict) -> Dict:
    """
    Task to classify a single email
    
    Args:
        agent: The email classifier agent
        email: Email dictionary with subject, from, body, etc.
        
    Returns:
        Classification result dictionary
    """
    subject = email.get('subject', '')
    from_address = email.get('from', '')
    body = email.get('text', '') or email.get('body', '')
    
    # Truncate body if too long
    if len(body) > 2000:
        body = body[:2000] + "..."
    
    prompt = f"""
Analyze this email and determine:
1. Is it job-related? (yes/no)
2. If yes, what type is it? Choose from:
   - application_confirmation: Automated confirmation of application receipt
   - rejection: Rejection email
   - interview_request: Interview invitation or scheduling
   - offer: Job offer
   - follow_up: Follow-up from recruiter
   - general: Other job-related communication
   - not_job_related: Not related to job applications

Email Details:
Subject: {subject}
From: {from_address}
Body: {body}

Respond in JSON format:
{{
    "is_job_related": true/false,
    "classification": "type",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}
"""
    
    try:
        response = agent.run(prompt)
        
        # Parse the response
        # The response might be wrapped in markdown code blocks
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
        
        result = json.loads(response_text)
        
        return {
            'message_id': email.get('message_id'),
            'is_job_related': result.get('is_job_related', False),
            'classification': result.get('classification', 'unknown'),
            'confidence': result.get('confidence', 0.0),
            'reasoning': result.get('reasoning', ''),
        }
        
    except Exception as e:
        print(f"✗ Error classifying email: {e}")
        return {
            'message_id': email.get('message_id'),
            'is_job_related': False,
            'classification': 'error',
            'confidence': 0.0,
            'reasoning': f'Classification error: {str(e)}',
        }


def classify_emails_batch(agent: Agent, emails: list) -> list:
    """
    Classify multiple emails
    
    Args:
        agent: The email classifier agent
        emails: List of email dictionaries
        
    Returns:
        List of classification results
    """
    print(f"\n{'='*60}")
    print(f"🤖 Email Classifier Agent: Classifying {len(emails)} emails")
    print(f"{'='*60}\n")
    
    results = []
    for i, email in enumerate(emails, 1):
        print(f"Classifying email {i}/{len(emails)}: {email.get('subject', 'No subject')[:50]}...")
        result = classify_email_task(agent, email)
        results.append(result)
        
        if result['is_job_related']:
            print(f"  ✓ Job-related: {result['classification']} (confidence: {result['confidence']:.2f})")
        else:
            print(f"  ✗ Not job-related")
    
    job_related_count = sum(1 for r in results if r['is_job_related'])
    print(f"\n✓ Classification complete: {job_related_count}/{len(emails)} job-related emails found")
    
    return results


if __name__ == "__main__":
    # Test the email classifier agent
    agent = create_email_classifier_agent()
    print(f"Created agent: {agent.name}")
    
    # Test with a sample email
    test_email = {
        'message_id': 'test123',
        'subject': 'Thank you for your application - Software Engineer',
        'from': 'noreply@company.com',
        'body': 'Thank you for applying to the Software Engineer position at our company. We have received your application and will review it shortly.'
    }
    
    result = classify_email_task(agent, test_email)
    print(f"\nClassification result:")
    print(json.dumps(result, indent=2))
