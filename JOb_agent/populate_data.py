import os
import random
from datetime import datetime, timedelta
from models.database import init_database, get_session, JobApplication, EmailLog

# Data lists
COMPANIES = [
    "Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix", "Tesla", 
    "Uber", "Airbnb", "Stripe", "Coinbase", "Spotify", "Shopify", "Slack",
    "Zoom", "Twilio", "Atlassian", "Salesforce", "Oracle", "IBM", "Intel",
    "Nvidia", "Adobe", "Intuit", "Square", "Twitter", "Snap", "Pinterest",
    "Lyft", "DoorDash", "Instacart", "Robinhood", "Dropbox", "Box", "Okta"
]

ROLES = [
    "Software Engineer", "Senior Software Engineer", "Product Manager", 
    "Data Scientist", "Machine Learning Engineer", "DevOps Engineer",
    "Frontend Engineer", "Backend Engineer", "Full Stack Engineer",
    "Engineering Manager", "Product Designer", "UX Researcher",
    "Technical Program Manager", "Solutions Architect", "Developer Advocate"
]

LOCATIONS = [
    "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
    "Remote", "Los Angeles, CA", "Boston, MA", "Chicago, IL", "Denver, CO",
    "London, UK", "Toronto, ON", "Vancouver, BC", "Berlin, DE", "Singapore"
]

STATUSES = [
    "applied", "interview_scheduled", "offer_received", "rejected"
]

# Weights for statuses to make it realistic
STATUS_WEIGHTS = [0.5, 0.2, 0.1, 0.2]

def generate_email_data(company, status, date):
    """Generate realistic email data based on status"""
    message_id = f"<{random.randint(10000000, 99999999)}.{random.randint(100000, 999999)}@mail.{company.lower()}.com>"
    
    if status == "applied":
        subject = f"Application Received - {company}"
        body = f"Thank you for applying to {company}. We have received your application and will review it shortly."
        from_addr = f"careers@{company.lower()}.com"
    elif status == "interview_scheduled":
        subject = f"Interview Invitation - {company}"
        body = f"We would like to invite you to an interview at {company}. Please let us know your availability."
        from_addr = f"recruiting@{company.lower()}.com"
    elif status == "offer_received":
        subject = f"Offer Letter - {company}"
        body = f"Congratulations! We are pleased to offer you a position at {company}. Please find the details attached."
        from_addr = f"hr@{company.lower()}.com"
    elif status == "rejected":
        subject = f"Update on your application - {company}"
        body = f"Thank you for your interest in {company}. Unfortunately, we have decided to move forward with other candidates."
        from_addr = f"no-reply@{company.lower()}.com"
    else:
        subject = f"Job Application Update - {company}"
        body = "Update regarding your application."
        from_addr = f"jobs@{company.lower()}.com"
        
    return {
        "subject": subject,
        "body": body,
        "from": from_addr,
        "message_id": message_id
    }

def populate():
    print("Initializing database...")
    init_database()
    session = get_session()
    
    # Clear existing data
    print("Clearing existing data...")
    session.query(JobApplication).delete()
    session.query(EmailLog).delete()
    session.commit()
    
    print("Generating data...")
    
    # Generate ~50 applications
    num_apps = 50
    start_date = datetime.now() - timedelta(days=90)
    
    for _ in range(num_apps):
        company = random.choice(COMPANIES)
        role = random.choice(ROLES)
        location = random.choice(LOCATIONS)
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
        
        # Random date within last 90 days
        days_ago = random.randint(0, 90)
        app_date = start_date + timedelta(days=days_ago)
        last_updated = app_date + timedelta(days=random.randint(0, 5))
        
        email_data = generate_email_data(company, status, app_date)
        
        # Create Job Application
        app = JobApplication(
            company_name=company,
            role_title=role,
            status=status,
            application_date=app_date,
            last_updated=last_updated,
            email_subject=email_data["subject"],
            email_body=email_data["body"],
            email_from=email_data["from"],
            email_date=app_date,
            email_message_id=email_data["message_id"],
            location=location,
            salary_range=f"${random.randint(120, 200)}k - ${random.randint(200, 300)}k",
            application_url=f"https://careers.{company.lower()}.com/jobs/{random.randint(1000, 9999)}",
            notes=f"Applied via LinkedIn. {random.choice(['Referral', 'Direct Apply', 'Recruiter reachout'])}."
        )
        session.add(app)
        
        # Create Email Log
        email_log = EmailLog(
            message_id=email_data["message_id"],
            subject=email_data["subject"],
            from_address=email_data["from"],
            date=app_date,
            is_job_related=1,
            classification="job_application",
            processed_date=datetime.now()
        )
        session.add(email_log)
        
    # Add some non-job emails to logs
    for _ in range(20):
        company = random.choice(COMPANIES)
        days_ago = random.randint(0, 90)
        email_date = start_date + timedelta(days=days_ago)
        message_id = f"<{random.randint(10000000, 99999999)}.{random.randint(100000, 999999)}@mail.spam.com>"
        
        email_log = EmailLog(
            message_id=message_id,
            subject=f"Newsletter from {company}",
            from_address=f"news@{company.lower()}.com",
            date=email_date,
            is_job_related=0,
            classification="newsletter",
            processed_date=datetime.now()
        )
        session.add(email_log)
        
    session.commit()
    print(f"Successfully created {num_apps} job applications and {num_apps + 20} email logs.")
    session.close()

if __name__ == "__main__":
    populate()
