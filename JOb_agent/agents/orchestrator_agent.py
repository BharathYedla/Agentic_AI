"""
Orchestrator Agent - Coordinates all agents in the job tracking workflow
"""
from agno.agent import Agent
from agents.email_monitor_agent import create_email_monitor_agent, fetch_emails_task
from agents.email_classifier_agent import create_email_classifier_agent, classify_emails_batch
from agents.data_extractor_agent import create_data_extractor_agent, extract_data_batch
from agents.database_manager_agent import create_database_manager_agent, save_applications_batch, get_statistics
from typing import Dict, List


def create_orchestrator_agent() -> Agent:
    """
    Create an orchestrator agent that coordinates all other agents
    
    Returns:
        Configured Agent instance
    """
    agent = Agent(
        name="Orchestrator Agent",
        role="Workflow Coordination Specialist",
        goal="Coordinate all agents to efficiently process job application emails",
        backstory="""You are an expert at coordinating complex workflows. You 
        manage the entire job tracking pipeline, ensuring each agent performs 
        its task efficiently and data flows smoothly between agents.""",
        verbose=True,
        allow_delegation=True,
    )
    
    return agent


def run_job_tracking_workflow(
    orchestrator: Agent,
    mode: str = 'recent',
    days: int = 7
) -> Dict:
    """
    Run the complete job tracking workflow
    
    Args:
        orchestrator: The orchestrator agent
        mode: Email fetching mode ('recent', 'unread', 'all')
        days: Number of days to look back (for 'recent' mode)
        
    Returns:
        Dictionary with workflow results and statistics
    """
    print(f"\n{'='*80}")
    print(f"🚀 ORCHESTRATOR: Starting Job Tracking Workflow")
    print(f"   Mode: {mode}, Days: {days}")
    print(f"{'='*80}\n")
    
    results = {
        'emails_fetched': 0,
        'job_related_emails': 0,
        'applications_saved': 0,
        'errors': [],
    }
    
    try:
        # Step 1: Create all agents
        print("📋 Step 1: Initializing agents...")
        email_monitor = create_email_monitor_agent()
        email_classifier = create_email_classifier_agent()
        data_extractor = create_data_extractor_agent()
        database_manager = create_database_manager_agent()
        print("✓ All agents initialized\n")
        
        # Step 2: Fetch emails
        print("📋 Step 2: Fetching emails...")
        emails = fetch_emails_task(email_monitor, days=days, mode=mode)
        results['emails_fetched'] = len(emails)
        
        if not emails:
            print("ℹ No emails found. Workflow complete.\n")
            return results
        
        # Step 3: Classify emails
        print("\n📋 Step 3: Classifying emails...")
        classifications = classify_emails_batch(email_classifier, emails)
        
        # Filter job-related emails
        job_related_data = [
            (email, classification)
            for email, classification in zip(emails, classifications)
            if classification.get('is_job_related', False)
        ]
        results['job_related_emails'] = len(job_related_data)
        
        if not job_related_data:
            print("ℹ No job-related emails found. Workflow complete.\n")
            return results
        
        job_emails, job_classifications = zip(*job_related_data)
        
        # Step 4: Extract data
        print("\n📋 Step 4: Extracting structured data...")
        extracted_data_list = extract_data_batch(
            data_extractor,
            list(job_emails),
            list(job_classifications)
        )
        
        if not extracted_data_list:
            print("ℹ No data extracted. Workflow complete.\n")
            return results
        
        # Step 5: Save to database
        print("\n📋 Step 5: Saving to database...")
        saved_ids = save_applications_batch(database_manager, extracted_data_list)
        results['applications_saved'] = len(saved_ids)
        
        # Step 6: Get final statistics
        print("\n📋 Step 6: Generating statistics...")
        stats = get_statistics(database_manager)
        results['statistics'] = stats
        
        # Print summary
        print(f"\n{'='*80}")
        print(f"✅ WORKFLOW COMPLETE - Summary")
        print(f"{'='*80}")
        print(f"📧 Emails fetched: {results['emails_fetched']}")
        print(f"🎯 Job-related emails: {results['job_related_emails']}")
        print(f"💾 Applications saved/updated: {results['applications_saved']}")
        print(f"\n📊 Database Statistics:")
        print(f"   Total applications: {stats.get('total_applications', 0)}")
        print(f"   By status:")
        for status, count in stats.get('by_status', {}).items():
            print(f"      - {status}: {count}")
        print(f"{'='*80}\n")
        
        return results
        
    except Exception as e:
        error_msg = f"Error in workflow: {str(e)}"
        print(f"\n✗ {error_msg}\n")
        results['errors'].append(error_msg)
        return results


def run_continuous_monitoring(
    orchestrator: Agent,
    interval_seconds: int = 3600
):
    """
    Run continuous monitoring of emails
    
    Args:
        orchestrator: The orchestrator agent
        interval_seconds: Time between checks in seconds
    """
    import time
    from datetime import datetime
    
    print(f"\n{'='*80}")
    print(f"🔄 CONTINUOUS MONITORING MODE")
    print(f"   Checking every {interval_seconds} seconds ({interval_seconds/60:.0f} minutes)")
    print(f"   Press Ctrl+C to stop")
    print(f"{'='*80}\n")
    
    try:
        while True:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running workflow...")
            run_job_tracking_workflow(orchestrator, mode='unread')
            
            print(f"\n⏰ Next check in {interval_seconds/60:.0f} minutes...")
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 Monitoring stopped by user")


def run_scheduled_monitoring(
    orchestrator: Agent,
    interval_seconds: int = 3600
):
    """
    Run scheduled monitoring using the schedule library
    
    Args:
        orchestrator: The orchestrator agent
        interval_seconds: Time between checks in seconds
    """
    import schedule
    import time
    from datetime import datetime
    
    def job():
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running scheduled workflow...")
        run_job_tracking_workflow(orchestrator, mode='unread')
    
    # Schedule the job
    schedule.every(interval_seconds).seconds.do(job)
    
    print(f"\n{'='*80}")
    print(f"📅 SCHEDULED MONITORING MODE")
    print(f"   Checking every {interval_seconds} seconds ({interval_seconds/60:.0f} minutes)")
    print(f"   Press Ctrl+C to stop")
    print(f"{'='*80}\n")
    
    # Run once immediately
    job()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n🛑 Monitoring stopped by user")


if __name__ == "__main__":
    # Test the orchestrator
    orchestrator = create_orchestrator_agent()
    print(f"Created agent: {orchestrator.name}")
    
    # Run a single workflow
    results = run_job_tracking_workflow(orchestrator, mode='recent', days=7)
