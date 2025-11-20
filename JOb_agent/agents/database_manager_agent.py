"""
Database Manager Agent - Manages all database operations for job applications
"""
from agno.agent import Agent
from models.database import JobApplication, EmailLog, get_session
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


def save_application_task(agent: Agent, extracted_data: Dict) -> Optional[int]:
    """
    Task to save or update a job application in the database
    
    Args:
        agent: The database manager agent
        extracted_data: Extracted data dictionary from data extractor agent
        
    Returns:
        Application ID if successful, None otherwise
    """
    session = get_session()
    
    try:
        message_id = extracted_data.get('email_message_id')
        
        # Check if this email has already been processed
        existing_log = session.query(EmailLog).filter_by(message_id=message_id).first()
        if existing_log:
            print(f"  ℹ Email {message_id} already processed, skipping...")
            return None
        
        # Check if application already exists for this company and role
        company = extracted_data.get('company_name')
        role = extracted_data.get('role_title')
        
        if not company or not role:
            print(f"  ✗ Missing company or role information, skipping...")
            return None
        
        existing_app = session.query(JobApplication).filter_by(
            company_name=company,
            role_title=role
        ).first()
        
        if existing_app:
            # Update existing application
            print(f"  ↻ Updating existing application: {company} - {role}")
            
            # Update status if it's a progression
            status_priority = {
                'applied': 1,
                'in_progress': 2,
                'follow_up_needed': 3,
                'interview_scheduled': 4,
                'offer_received': 5,
                'rejected': 6,
            }
            
            current_priority = status_priority.get(existing_app.status, 0)
            new_priority = status_priority.get(extracted_data.get('status'), 0)
            
            if new_priority >= current_priority:
                existing_app.status = extracted_data.get('status', existing_app.status)
            
            # Update other fields if they have new information
            if extracted_data.get('location'):
                existing_app.location = extracted_data['location']
            if extracted_data.get('salary_range'):
                existing_app.salary_range = extracted_data['salary_range']
            if extracted_data.get('application_url'):
                existing_app.application_url = extracted_data['application_url']
            
            # Append to notes
            new_note = f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {extracted_data.get('classification', 'Update')}: {extracted_data.get('additional_notes', '')}"
            existing_app.notes = (existing_app.notes or '') + new_note
            
            # Update metadata
            if not existing_app.metadata:
                existing_app.metadata = {}
            existing_app.metadata['last_email_subject'] = extracted_data.get('email_subject')
            existing_app.metadata['last_email_from'] = extracted_data.get('email_from')
            
            existing_app.last_updated = datetime.utcnow()
            
            app_id = existing_app.id
            
        else:
            # Create new application
            print(f"  ✓ Creating new application: {company} - {role}")
            
            # Parse application date
            app_date = None
            if extracted_data.get('application_date'):
                try:
                    app_date = datetime.strptime(extracted_data['application_date'], '%Y-%m-%d')
                except:
                    pass
            
            # Parse email date
            email_date = None
            if extracted_data.get('email_date'):
                if isinstance(extracted_data['email_date'], datetime):
                    email_date = extracted_data['email_date']
                else:
                    try:
                        email_date = datetime.fromisoformat(str(extracted_data['email_date']))
                    except:
                        pass
            
            new_app = JobApplication(
                company_name=company,
                role_title=role,
                status=extracted_data.get('status', 'applied'),
                application_date=app_date,
                email_subject=extracted_data.get('email_subject'),
                email_body=extracted_data.get('email_body', ''),
                email_from=extracted_data.get('email_from'),
                email_date=email_date,
                email_message_id=message_id,
                location=extracted_data.get('location'),
                salary_range=extracted_data.get('salary_range'),
                application_url=extracted_data.get('application_url'),
                metadata={
                    'classification': extracted_data.get('classification'),
                    'next_steps': extracted_data.get('next_steps'),
                    'interview_datetime': extracted_data.get('interview_datetime'),
                    'contact_person': extracted_data.get('contact_person'),
                },
                notes=extracted_data.get('additional_notes', ''),
            )
            
            session.add(new_app)
            session.flush()
            app_id = new_app.id
        
        # Log the email as processed
        email_log = EmailLog(
            message_id=message_id,
            subject=extracted_data.get('email_subject'),
            from_address=extracted_data.get('email_from'),
            date=email_date,
            is_job_related=1,
            classification=extracted_data.get('classification'),
        )
        session.add(email_log)
        
        session.commit()
        print(f"  ✓ Saved to database (ID: {app_id})")
        return app_id
        
    except IntegrityError as e:
        session.rollback()
        print(f"  ✗ Database integrity error: {e}")
        return None
    except Exception as e:
        session.rollback()
        print(f"  ✗ Error saving to database: {e}")
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
    session = get_session()
    
    try:
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
