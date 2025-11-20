"""
Database models for job application tracking
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class JobApplication(Base):
    """Model for storing job application information"""
    
    __tablename__ = 'job_applications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Core Information
    company_name = Column(String(255), nullable=False)
    role_title = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)  # applied, rejected, interview, offer, etc.
    
    # Dates
    application_date = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Email Information
    email_subject = Column(String(500), nullable=True)
    email_body = Column(Text, nullable=True)
    email_from = Column(String(255), nullable=True)
    email_date = Column(DateTime, nullable=True)
    email_message_id = Column(String(255), unique=True, nullable=True)
    
    # Additional Information
    job_description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    salary_range = Column(String(100), nullable=True)
    application_url = Column(String(500), nullable=True)
    
    # Metadata (JSON field for flexible data storage)
    extra_data = Column(JSON, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<JobApplication(company='{self.company_name}', role='{self.role_title}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'company_name': self.company_name,
            'role_title': self.role_title,
            'status': self.status,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'email_subject': self.email_subject,
            'email_from': self.email_from,
            'email_date': self.email_date.isoformat() if self.email_date else None,
            'location': self.location,
            'salary_range': self.salary_range,
            'application_url': self.application_url,
            'extra_data': self.extra_data,
            'notes': self.notes
        }


class EmailLog(Base):
    """Model for logging all processed emails"""
    
    __tablename__ = 'email_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String(255), unique=True, nullable=False)
    subject = Column(String(500), nullable=True)
    from_address = Column(String(255), nullable=True)
    date = Column(DateTime, nullable=True)
    is_job_related = Column(Integer, default=0)  # 0 = No, 1 = Yes
    classification = Column(String(50), nullable=True)
    processed_date = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<EmailLog(message_id='{self.message_id}', is_job_related={self.is_job_related})>"


# Database setup
def get_database_url():
    """Get database URL from environment or use default"""
    return os.getenv('DATABASE_URL', 'sqlite:///job_tracker.db')


def create_db_engine():
    """Create database engine"""
    database_url = get_database_url()
    engine = create_engine(database_url, echo=False)
    return engine


def init_database():
    """Initialize database and create all tables"""
    engine = create_db_engine()
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")
    return engine


def get_session():
    """Get database session"""
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    # Initialize database when run directly
    init_database()
    print("Database tables created successfully!")
