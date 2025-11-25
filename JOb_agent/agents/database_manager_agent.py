"""
Database Manager Agent - Manages all database operations for job applications
"""
from agno.agent import Agent
try:
    from models.database import JobApplication, EmailLog, get_session
except ImportError:
    # Handle backend environment where models.database is different
    JobApplication = None
    EmailLog = None
    get_session = None
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def create_database_manager_agent() -> Agent:
    """
    Create an agent that manages database operations
    
    Returns:
        Configured Agent instance
    """
    agent = Agent(
        name="Database Manager Agent",
        role="Database Management Specialist",
        description="Efficiently store and manage job application data",
        instructions="""You are an expert at managing databases and ensuring data 
        integrity. You handle all database operations including creating, updating, 
        and querying job application records.""",
        debug_mode=True,
    )
    
    return agent


def get_local_session():
    """Get database session handling both standalone and backend modes"""
    try:
        # Try to use backend models if available
        from ios_app.backend.models.database import JobApplication as BackendJobApplication
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        import os
        
        # Use absolute path to backend DB to avoid CWD issues
        # Assuming we are running from project root or backend dir
        # Try to find the DB file
        possible_paths = [
            "ios_app/backend/job_tracker.db",
            "../ios_app/backend/job_tracker.db",
            "/Users/bharath/Documents/Git/AI_Agents/Multi_Agent/Job_agent/Agentic_AI-1/JOb_agent/ios_app/backend/job_tracker.db"
        ]
        
        db_path = "ios_app/backend/job_tracker.db"
        for p in possible_paths:
            if os.path.exists(p):
                db_path = p
                break
                
        db_url = f"sqlite:///{db_path}"
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        return Session(), True # (session, is_backend)
    except ImportError:
        from models.database import get_session as original_get_session
        return original_get_session(), False

def save_application_task(agent: Agent, extracted_data: Dict) -> Optional[int]:
    """
    Task to save or update a job application in the database
    """
    session, is_backend = get_local_session()
    
    try:
        if is_backend:
            from ios_app.backend.models.database import JobApplication, EmailLog, ApplicationStatus
            
            message_id = extracted_data.get('email_message_id')
            company = extracted_data.get('company_name')
            role = extracted_data.get('role_title')
            
            if not company or not role:
                print(f"  ✗ Missing company or role information, skipping...")
                return None
            
            # Check existing
            existing_app = session.query(JobApplication).filter_by(
                company_name=company,
                role_title=role,
                user_id=1
            ).first()
            
            if existing_app:
                print(f"  ↻ Updating existing application: {company} - {role}")
                # Update status logic could go here
                # For now just update notes
                new_note = f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {extracted_data.get('classification', 'Update')}: {extracted_data.get('additional_notes', '')}"
                existing_app.notes = (existing_app.notes or '') + new_note
                app_id = existing_app.id
            else:
                print(f"  ✓ Creating new application: {company} - {role}")
                
                # Map status string to Enum
                status_str = extracted_data.get('status', 'applied').lower()
                status_enum = ApplicationStatus.APPLIED
                if 'interview' in status_str:
                    status_enum = ApplicationStatus.INTERVIEW_SCHEDULED
                elif 'offer' in status_str:
                    status_enum = ApplicationStatus.OFFER_RECEIVED
                elif 'reject' in status_str:
                    status_enum = ApplicationStatus.REJECTED
                
                new_app = JobApplication(
                    user_id=1,
                    company_name=company,
                    role_title=role,
                    status=status_enum,
                    job_description=extracted_data.get('email_body', ''),
                    location=extracted_data.get('location'),
                    application_url=extracted_data.get('application_url'),
                    notes=extracted_data.get('additional_notes', ''),
                    email_subject=extracted_data.get('email_subject'),
                    email_from=extracted_data.get('email_from'),
                    email_message_id=message_id,
                )
                session.add(new_app)
                session.flush()
                app_id = new_app.id
            
            # Log email
            # Check if email log exists
            existing_log = session.query(EmailLog).filter_by(message_id=message_id).first()
            if not existing_log:
                email_log = EmailLog(
                    message_id=message_id,
                    application_id=app_id,
                    subject=extracted_data.get('email_subject'),
                    from_address=extracted_data.get('email_from'),
                    is_job_related=True,
                    # classification=extracted_data.get('classification') # Enum mismatch potential, skip for now
                )
                session.add(email_log)
            
            session.commit()
            print(f"  ✓ Saved to backend database (ID: {app_id})")
            return app_id
            
        else:
            print("  ✗ Backend models not available. Standalone mode not fully implemented in this patch.")
            return None
        
    except Exception as e:
        session.rollback()
        print(f"  ✗ Error saving to database: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        session.close()


def save_applications_batch(agent: Agent, extracted_data_list: List[Dict]) -> List[int]:
    """
    Save multiple applications to the database
    
    Args:
        agent: The database manager agent
        extracted_data_list: List of extracted data dictionaries
        
    Returns:
        List of application IDs
    """
    print(f"\n{'='*60}")
    print(f"💾 Database Manager Agent: Saving {len(extracted_data_list)} applications")
    print(f"{'='*60}\n")
    
    saved_ids = []
    for i, data in enumerate(extracted_data_list, 1):
        print(f"Processing {i}/{len(extracted_data_list)}: {data.get('company_name', 'Unknown')} - {data.get('role_title', 'Unknown')}")
        app_id = save_application_task(agent, data)
        if app_id:
            saved_ids.append(app_id)
    
    print(f"\n✓ Database operations complete: {len(saved_ids)} applications saved/updated")
    return saved_ids


def get_all_applications(agent: Agent) -> List[Dict]:
    """
    Get all job applications from the database
    
    Args:
        agent: The database manager agent
        
    Returns:
        List of application dictionaries
    """
    session = get_session()
    
    try:
        applications = session.query(JobApplication).all()
        return [app.to_dict() for app in applications]
    except Exception as e:
        print(f"✗ Error fetching applications: {e}")
        return []
    finally:
        session.close()


def get_applications_by_status(agent: Agent, status: str) -> List[Dict]:
    """
    Get job applications by status
    
    Args:
        agent: The database manager agent
        status: Application status to filter by
        
    Returns:
        List of application dictionaries
    """
    session = get_session()
    
    try:
        applications = session.query(JobApplication).filter_by(status=status).all()
        return [app.to_dict() for app in applications]
    except Exception as e:
        print(f"✗ Error fetching applications: {e}")
        return []
    finally:
        session.close()


def get_statistics(agent: Agent) -> Dict:
    """
    Get statistics about job applications
    
    Args:
        agent: The database manager agent
        
    Returns:
        Dictionary with statistics
    """
    session, is_backend = get_local_session()
    
    try:
        if is_backend:
            from ios_app.backend.models.database import JobApplication
            total = session.query(JobApplication).count()
            
            stats = {
                'total_applications': total,
                'by_status': {},
            }
            
            # Count by status
            from sqlalchemy import func
            status_counts = session.query(
                JobApplication.status,
                func.count(JobApplication.id)
            ).group_by(JobApplication.status).all()
            
            for status, count in status_counts:
                stats['by_status'][status] = count
            
            return stats
        else:
            # Original logic
            if not get_session:
                return {}
                
            total = session.query(JobApplication).count()
            
            stats = {
                'total_applications': total,
                'by_status': {},
            }
            
            # Count by status
            from sqlalchemy import func
            status_counts = session.query(
                JobApplication.status,
                func.count(JobApplication.id)
            ).group_by(JobApplication.status).all()
            
            for status, count in status_counts:
                stats['by_status'][status] = count
            
            return stats
        
    except Exception as e:
        print(f"✗ Error getting statistics: {e}")
        return {}
    finally:
        session.close()


if __name__ == "__main__":
    # Test the database manager agent
    from models.database import init_database
    
    # Initialize database
    init_database()
    
    agent = create_database_manager_agent()
    print(f"Created agent: {agent.name}")
    
    # Get statistics
    stats = get_statistics(agent)
    print(f"\nDatabase statistics:")
    print(f"  Total applications: {stats.get('total_applications', 0)}")
    print(f"  By status: {stats.get('by_status', {})}")
