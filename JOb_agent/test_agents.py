#!/usr/bin/env python3
"""
Unit Testing Script for Job Application Email Tracker Agents

This script tests each agent individually to ensure they work correctly.
Run this before testing the full orchestration workflow.
"""

import sys
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

console = Console()


def print_header(title):
    """Print a formatted header"""
    console.print(f"\n[bold cyan]{'='*70}[/bold cyan]")
    console.print(f"[bold yellow]{title}[/bold yellow]")
    console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")


def print_success(message):
    """Print success message"""
    console.print(f"[green]✓[/green] {message}")


def print_error(message):
    """Print error message"""
    console.print(f"[red]✗[/red] {message}")


def print_info(message):
    """Print info message"""
    console.print(f"[blue]ℹ[/blue] {message}")


def test_config():
    """Test 1: Configuration Validation"""
    print_header("Test 1: Configuration Validation")
    
    try:
        from utils.config import load_config, validate_config
        
        print_info("Loading configuration...")
        config = load_config()
        
        print_info("Validating configuration...")
        is_valid = validate_config()
        
        if is_valid:
            print_success("Configuration is valid")
            print_info(f"Email: {config.email_address}")
            print_info(f"OpenAI Key: {config.openai_api_key[:10]}..." if config.openai_api_key else "Not set")
            return True
        else:
            print_error("Configuration validation failed")
            print_info("Please check your .env file")
            return False
            
    except Exception as e:
        print_error(f"Configuration test failed: {e}")
        return False


def test_database():
    """Test 2: Database Initialization"""
    print_header("Test 2: Database Initialization")
    
    try:
        from models.database import init_database, get_session
        from models.database import JobApplication
        
        print_info("Initializing database...")
        init_database()
        print_success("Database initialized")
        
        print_info("Testing database connection...")
        session = get_session()
        
        # Try to query
        count = session.query(JobApplication).count()
        print_success(f"Database connection successful")
        print_info(f"Current applications in database: {count}")
        
        session.close()
        return True
        
    except Exception as e:
        print_error(f"Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_email_monitor_agent():
    """Test 3: Email Monitor Agent"""
    print_header("Test 3: Email Monitor Agent")
    
    try:
        from agents.email_monitor_agent import create_email_monitor_agent
        
        print_info("Creating Email Monitor Agent...")
        agent = create_email_monitor_agent()
        print_success("Email Monitor Agent created")
        
        print_info("Testing email connection (fetching 1 recent email)...")
        # This will attempt to connect to the email server
        result = agent.run(
            "Fetch the most recent email from the last 1 day",
            stream=False
        )
        
        if result and not result.content.startswith("Error"):
            print_success("Email Monitor Agent working correctly")
            print_info(f"Response: {result.content[:100]}...")
            return True
        else:
            print_error("Email Monitor Agent returned an error")
            print_info(f"Response: {result.content if result else 'No response'}")
            return False
            
    except Exception as e:
        print_error(f"Email Monitor Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_email_classifier_agent():
    """Test 4: Email Classifier Agent"""
    print_header("Test 4: Email Classifier Agent")
    
    try:
        from agents.email_classifier_agent import create_email_classifier_agent
        
        print_info("Creating Email Classifier Agent...")
        agent = create_email_classifier_agent()
        print_success("Email Classifier Agent created")
        
        # Test with sample email
        test_email = {
            "subject": "Thank you for your application to Software Engineer at Google",
            "body": "Dear Candidate, We have received your application for the Software Engineer position. We will review it and get back to you soon."
        }
        
        print_info("Testing classification with sample email...")
        result = agent.run(
            f"Classify this email:\nSubject: {test_email['subject']}\nBody: {test_email['body']}",
            stream=False
        )
        
        if result:
            print_success("Email Classifier Agent working correctly")
            print_info(f"Classification result: {result.content[:200]}...")
            return True
        else:
            print_error("Email Classifier Agent returned no result")
            return False
            
    except Exception as e:
        print_error(f"Email Classifier Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_extractor_agent():
    """Test 5: Data Extractor Agent"""
    print_header("Test 5: Data Extractor Agent")
    
    try:
        from agents.data_extractor_agent import create_data_extractor_agent
        
        print_info("Creating Data Extractor Agent...")
        agent = create_data_extractor_agent()
        print_success("Data Extractor Agent created")
        
        # Test with sample email
        test_email = {
            "subject": "Interview invitation - Senior Developer at Microsoft",
            "body": "Dear John, We are pleased to invite you for an interview for the Senior Developer position at Microsoft. The interview is scheduled for next Monday."
        }
        
        print_info("Testing data extraction with sample email...")
        result = agent.run(
            f"Extract structured data from this email:\nSubject: {test_email['subject']}\nBody: {test_email['body']}",
            stream=False
        )
        
        if result:
            print_success("Data Extractor Agent working correctly")
            print_info(f"Extraction result: {result.content[:200]}...")
            return True
        else:
            print_error("Data Extractor Agent returned no result")
            return False
            
    except Exception as e:
        print_error(f"Data Extractor Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_manager_agent():
    """Test 6: Database Manager Agent"""
    print_header("Test 6: Database Manager Agent")
    
    try:
        from agents.database_manager_agent import create_database_manager_agent
        
        print_info("Creating Database Manager Agent...")
        agent = create_database_manager_agent()
        print_success("Database Manager Agent created")
        
        print_info("Testing database query...")
        result = agent.run(
            "Get statistics about all job applications",
            stream=False
        )
        
        if result:
            print_success("Database Manager Agent working correctly")
            print_info(f"Query result: {result.content[:200]}...")
            return True
        else:
            print_error("Database Manager Agent returned no result")
            return False
            
    except Exception as e:
        print_error(f"Database Manager Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_orchestrator_agent():
    """Test 7: Orchestrator Agent"""
    print_header("Test 7: Orchestrator Agent")
    
    try:
        from agents.orchestrator_agent import create_orchestrator_agent
        
        print_info("Creating Orchestrator Agent...")
        agent = create_orchestrator_agent()
        print_success("Orchestrator Agent created")
        
        print_info("Orchestrator agent initialized successfully")
        print_info("Full workflow testing should be done via main.py")
        return True
            
    except Exception as e:
        print_error(f"Orchestrator Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and display summary"""
    console.print(Panel.fit(
        "[bold magenta]Job Application Email Tracker - Agent Testing Suite[/bold magenta]",
        border_style="magenta"
    ))
    
    tests = [
        ("Configuration", test_config),
        ("Database", test_database),
        ("Email Monitor Agent", test_email_monitor_agent),
        ("Email Classifier Agent", test_email_classifier_agent),
        ("Data Extractor Agent", test_data_extractor_agent),
        ("Database Manager Agent", test_database_manager_agent),
        ("Orchestrator Agent", test_orchestrator_agent),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except KeyboardInterrupt:
            print_error("\nTesting interrupted by user")
            sys.exit(1)
        except Exception as e:
            print_error(f"Unexpected error in {test_name}: {e}")
            results[test_name] = False
    
    # Display summary
    print_header("Test Summary")
    
    table = Table(title="Test Results", show_header=True, header_style="bold magenta")
    table.add_column("Test", style="cyan", width=30)
    table.add_column("Status", width=15)
    table.add_column("Result", width=20)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        if result:
            table.add_row(test_name, "[green]✓ PASSED[/green]", "[green]Success[/green]")
            passed += 1
        else:
            table.add_row(test_name, "[red]✗ FAILED[/red]", "[red]Failed[/red]")
            failed += 1
    
    console.print(table)
    
    # Final summary
    total = passed + failed
    console.print(f"\n[bold]Total Tests:[/bold] {total}")
    console.print(f"[green]Passed:[/green] {passed}")
    console.print(f"[red]Failed:[/red] {failed}")
    console.print(f"[cyan]Success Rate:[/cyan] {(passed/total*100):.1f}%\n")
    
    if failed == 0:
        console.print(Panel.fit(
            "[bold green]✓ All tests passed! Your Job Agent is ready to use.[/bold green]",
            border_style="green"
        ))
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("1. Run a one-time scan: [cyan]python main.py --mode once[/cyan]")
        console.print("2. View the dashboard: [cyan]python dashboard.py[/cyan]")
        console.print("3. Set up scheduled monitoring: [cyan]python main.py --mode scheduled[/cyan]")
        return 0
    else:
        console.print(Panel.fit(
            f"[bold red]✗ {failed} test(s) failed. Please fix the issues before proceeding.[/bold red]",
            border_style="red"
        ))
        console.print("\n[yellow]Troubleshooting tips:[/yellow]")
        console.print("1. Check your .env file configuration")
        console.print("2. Verify your email credentials")
        console.print("3. Ensure OpenAI API key is valid")
        console.print("4. Check the error messages above for details")
        return 1


if __name__ == "__main__":
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Testing interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)
