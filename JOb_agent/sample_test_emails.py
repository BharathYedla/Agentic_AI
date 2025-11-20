"""
Sample Test Email Generator

This script helps you create sample test emails to verify your Job Agent
is working correctly. You can send these to yourself to test the system.
"""

from datetime import datetime


SAMPLE_EMAILS = {
    "application_confirmation": {
        "subject": "Thank you for your application to Software Engineer at TechCorp",
        "body": """Dear Candidate,

Thank you for applying to the Software Engineer position at TechCorp. 

We have received your application and our team is currently reviewing it. 
We will get back to you within 2-3 weeks regarding the next steps.

Best regards,
TechCorp Recruiting Team
recruiting@techcorp.com
""",
        "expected_classification": "Application Confirmation",
        "expected_company": "TechCorp",
        "expected_role": "Software Engineer",
        "expected_status": "applied"
    },
    
    "interview_request": {
        "subject": "Interview Invitation - Senior Developer Role at InnovateLabs",
        "body": """Hi there,

We were impressed with your application for the Senior Developer position at InnovateLabs!

We would like to invite you for an interview. Please let us know your availability 
for next week (Monday-Friday, 10 AM - 4 PM).

The interview will be conducted via Zoom and will last approximately 1 hour.

Looking forward to speaking with you!

Best,
Sarah Johnson
Talent Acquisition Manager
InnovateLabs
sarah.johnson@innovatelabs.com
""",
        "expected_classification": "Interview Request",
        "expected_company": "InnovateLabs",
        "expected_role": "Senior Developer",
        "expected_status": "interview"
    },
    
    "rejection": {
        "subject": "Update on your application - Data Scientist at DataCo",
        "body": """Dear Applicant,

Thank you for your interest in the Data Scientist position at DataCo.

After careful consideration, we have decided to move forward with other candidates 
whose qualifications more closely match our current needs.

We appreciate the time you invested in the application process and wish you 
the best in your job search.

Sincerely,
DataCo HR Team
hr@dataco.com
""",
        "expected_classification": "Rejection",
        "expected_company": "DataCo",
        "expected_role": "Data Scientist",
        "expected_status": "rejected"
    },
    
    "job_offer": {
        "subject": "Job Offer - Product Manager at StartupXYZ",
        "body": """Congratulations!

We are delighted to extend an offer for the Product Manager position at StartupXYZ.

Offer Details:
- Position: Product Manager
- Start Date: March 1, 2024
- Salary: $120,000/year
- Benefits: Health insurance, 401k, unlimited PTO

Please review the attached offer letter and let us know your decision by Friday.

We're excited about the possibility of you joining our team!

Best regards,
Michael Chen
CEO, StartupXYZ
michael@startupxyz.com
""",
        "expected_classification": "Job Offer",
        "expected_company": "StartupXYZ",
        "expected_role": "Product Manager",
        "expected_status": "offer"
    },
    
    "follow_up": {
        "subject": "Following up on your application - Full Stack Developer",
        "body": """Hi,

I wanted to follow up on your application for the Full Stack Developer position 
at WebSolutions Inc.

We're currently in the final stages of our review process. I wanted to let you 
know that we're still very interested in your profile.

Could you please confirm your continued interest in this role? Also, would you 
be available for a quick call next week?

Thanks,
Lisa Martinez
Senior Recruiter
WebSolutions Inc.
lisa.martinez@websolutions.com
""",
        "expected_classification": "Follow-up",
        "expected_company": "WebSolutions Inc",
        "expected_role": "Full Stack Developer",
        "expected_status": "applied"
    },
    
    "assessment_request": {
        "subject": "Next Steps: Technical Assessment - Backend Engineer at CloudTech",
        "body": """Hello,

Thank you for your application to the Backend Engineer position at CloudTech.

As a next step in our hiring process, we would like you to complete a technical 
assessment. The assessment should take approximately 2-3 hours to complete.

You will have 7 days to complete the assessment from the time you receive the link.

Please click here to begin: [assessment link]

If you have any questions, please don't hesitate to reach out.

Best,
CloudTech Engineering Team
engineering@cloudtech.io
""",
        "expected_classification": "Assessment Request",
        "expected_company": "CloudTech",
        "expected_role": "Backend Engineer",
        "expected_status": "interview"
    }
}


def print_sample_email(email_type, email_data):
    """Print a sample email in a formatted way"""
    print("\n" + "="*70)
    print(f"EMAIL TYPE: {email_type.upper()}")
    print("="*70)
    print(f"\nSubject: {email_data['subject']}")
    print(f"\nBody:\n{email_data['body']}")
    print("\n" + "-"*70)
    print("EXPECTED RESULTS:")
    print("-"*70)
    print(f"Classification: {email_data['expected_classification']}")
    print(f"Company: {email_data['expected_company']}")
    print(f"Role: {email_data['expected_role']}")
    print(f"Status: {email_data['expected_status']}")
    print("="*70 + "\n")


def generate_email_file(email_type, email_data, output_dir="test_emails"):
    """Generate an .eml file that can be imported into email clients"""
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{output_dir}/{email_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.eml"
    
    eml_content = f"""From: noreply@example.com
To: your_email@example.com
Subject: {email_data['subject']}
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}
Content-Type: text/plain; charset=utf-8

{email_data['body']}
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(eml_content)
    
    return filename


def main():
    """Main function to display and optionally generate sample emails"""
    print("\n" + "="*70)
    print("JOB AGENT - SAMPLE TEST EMAILS")
    print("="*70)
    print("\nThese sample emails can be used to test your Job Agent system.")
    print("You can either:")
    print("  1. Send these to yourself manually")
    print("  2. Generate .eml files to import into your email client")
    print("  3. Use them as reference for what the system should detect")
    print("\n")
    
    # Display all sample emails
    for email_type, email_data in SAMPLE_EMAILS.items():
        print_sample_email(email_type, email_data)
    
    # Ask if user wants to generate .eml files
    print("\n" + "="*70)
    response = input("Generate .eml files for these emails? (y/n): ").lower().strip()
    
    if response == 'y':
        print("\nGenerating .eml files...")
        for email_type, email_data in SAMPLE_EMAILS.items():
            filename = generate_email_file(email_type, email_data)
            print(f"✓ Generated: {filename}")
        
        print("\n" + "="*70)
        print("FILES GENERATED SUCCESSFULLY!")
        print("="*70)
        print("\nYou can now:")
        print("  1. Import these .eml files into your email client")
        print("  2. Or copy the content and send as regular emails to yourself")
        print("  3. Then run: python main.py --mode once")
        print("\n")
    else:
        print("\nNo files generated. You can copy the email content above manually.")
    
    # Print testing instructions
    print("\n" + "="*70)
    print("TESTING INSTRUCTIONS")
    print("="*70)
    print("""
1. Send these sample emails to yourself (or import the .eml files)
2. Wait a few minutes for emails to arrive
3. Run the Job Agent: python main.py --mode once --days 1
4. Check the results in the dashboard: python dashboard.py
5. Verify that the agent correctly:
   - Identified all job-related emails
   - Classified them correctly
   - Extracted company names and roles
   - Set the appropriate status

Expected Results:
- 6 emails should be detected as job-related
- Each should be classified according to the "expected_classification" above
- Company names and roles should match the expected values
- Statuses should be set correctly (applied, interview, rejected, offer)
""")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
