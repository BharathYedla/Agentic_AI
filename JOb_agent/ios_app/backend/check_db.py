from sqlalchemy import create_engine, text
import os

db_path = "job_tracker.db"
engine = create_engine(f"sqlite:///{db_path}")

with engine.connect() as conn:
    print("Checking job_applications table:")
    result = conn.execute(text("SELECT count(*) FROM job_applications"))
    print(f"Total applications: {result.scalar()}")
    
    print("\nChecking email_logs table:")
    result = conn.execute(text("SELECT count(*) FROM email_logs"))
    total_emails = result.scalar()
    print(f"Total emails logged: {total_emails}")
    
    if total_emails > 0:
        print("\nRecent email logs:")
        result = conn.execute(text("SELECT subject, is_job_related, classification FROM email_logs ORDER BY id DESC LIMIT 5"))
        for row in result:
            print(f"- {row[0]} (Job Related: {row[1]}, Class: {row[2]})")
