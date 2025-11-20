"""
Main entry point for the Job Application Email Tracker
"""
import argparse
import sys
from models.database import init_database
from agents.orchestrator_agent import (
    create_orchestrator_agent,
    run_job_tracking_workflow,
    run_continuous_monitoring,
    run_scheduled_monitoring
)
from utils.config import validate_config


def main():
    """Main function to run the job tracker"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Job Application Email Tracker - Multi-Agent System'
    )
    parser.add_argument(
        '--mode',
        choices=['once', 'continuous', 'scheduled'],
        default='once',
        help='Monitoring mode: once (single run), continuous, or scheduled'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=3600,
        help='Check interval in seconds (for continuous/scheduled mode, default: 3600 = 1 hour)'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to look back for emails (default: 7)'
    )
    parser.add_argument(
        '--email-mode',
        choices=['recent', 'unread', 'all'],
        default='recent',
        help='Email fetching mode: recent, unread, or all'
    )
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize database and exit'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     Job Application Email Tracker - Multi-Agent System       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize database if requested
    if args.init_db:
        print("Initializing database...")
        init_database()
        print("✓ Database initialized successfully!")
        return 0
    
    # Validate configuration
    print("Validating configuration...")
    if not validate_config():
        print("\n✗ Configuration validation failed!")
        print("Please check your .env file and ensure all required fields are set.")
        print("See .env.example for reference.")
        return 1
    print("✓ Configuration valid\n")
    
    # Initialize database
    print("Initializing database...")
    init_database()
    print("✓ Database ready\n")
    
    # Create orchestrator agent
    orchestrator = create_orchestrator_agent()
    
    # Run based on mode
    try:
        if args.mode == 'once':
            print(f"Running single workflow (mode: {args.email_mode}, days: {args.days})...\n")
            results = run_job_tracking_workflow(
                orchestrator,
                mode=args.email_mode,
                days=args.days
            )
            
            if results.get('errors'):
                print("\n⚠️  Workflow completed with errors:")
                for error in results['errors']:
                    print(f"   - {error}")
                return 1
            
            return 0
            
        elif args.mode == 'continuous':
            run_continuous_monitoring(orchestrator, interval_seconds=args.interval)
            return 0
            
        elif args.mode == 'scheduled':
            run_scheduled_monitoring(orchestrator, interval_seconds=args.interval)
            return 0
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        return 0
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
