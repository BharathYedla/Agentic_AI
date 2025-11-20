"""
Initialize agents package
"""
from agents.email_monitor_agent import create_email_monitor_agent, fetch_emails_task
from agents.email_classifier_agent import create_email_classifier_agent, classify_email_task
from agents.data_extractor_agent import create_data_extractor_agent, extract_data_task
from agents.database_manager_agent import create_database_manager_agent, save_application_task
from agents.orchestrator_agent import create_orchestrator_agent, run_job_tracking_workflow

__all__ = [
    'create_email_monitor_agent',
    'fetch_emails_task',
    'create_email_classifier_agent',
    'classify_email_task',
    'create_data_extractor_agent',
    'extract_data_task',
    'create_database_manager_agent',
    'save_application_task',
    'create_orchestrator_agent',
    'run_job_tracking_workflow',
]
