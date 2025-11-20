"""
Database models for JobTracker backend
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
import enum
from datetime import datetime
from typing import Optional


class ApplicationStatus(str, enum.Enum):
    """Application status enum"""
    APPLIED = "applied"
    IN_PROGRESS = "in_progress"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    OFFER_RECEIVED = "offer_received"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class EmailClassification(str, enum.Enum):
    """Email classification enum"""
    APPLICATION_CONFIRMATION = "application_confirmation"
    REJECTION = "rejection"
    INTERVIEW_REQUEST = "interview_request"
    OFFER = "offer"
    FOLLOW_UP = "follow_up"
    GENERAL = "general"
    NOT_JOB_RELATED = "not_job_related"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Preferences
    preferences = Column(JSON, default={})
    
    # Relationships
    email_accounts = relationship("EmailAccount", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("JobApplication", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(email='{self.email}')>"


class EmailAccount(Base):
    """Email account model"""
    __tablename__ = "email_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Email configuration
    email_address = Column(String(255), nullable=False)
    provider = Column(String(50), nullable=False)  # gmail, outlook, yahoo, etc.
    imap_server = Column(String(255), nullable=False)
    imap_port = Column(Integer, nullable=False)
    
    # Encrypted credentials
    encrypted_password = Column(Text, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_sync = Column(DateTime(timezone=True), nullable=True)
    sync_enabled = Column(Boolean, default=True)
    
    # Settings
    sync_interval_minutes = Column(Integer, default=60)
    lookback_days = Column(Integer, default=30)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="email_accounts")
    
    def __repr__(self):
        return f"<EmailAccount(email='{self.email_address}')>"


class JobApplication(Base):
    """Job application model"""
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Core information
    company_name = Column(String(255), nullable=False, index=True)
    role_title = Column(String(255), nullable=False, index=True)
    status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.APPLIED, index=True)
    
    # Details
    job_description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    work_type = Column(String(50), nullable=True)  # remote, hybrid, onsite
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String(10), default="USD")
    
    # URLs
    application_url = Column(String(500), nullable=True)
    company_website = Column(String(500), nullable=True)
    
    # Dates
    application_date = Column(DateTime(timezone=True), nullable=True)
    deadline_date = Column(DateTime(timezone=True), nullable=True)
    interview_date = Column(DateTime(timezone=True), nullable=True)
    offer_date = Column(DateTime(timezone=True), nullable=True)
    
    # Email tracking
    email_subject = Column(String(500), nullable=True)
    email_from = Column(String(255), nullable=True)
    email_message_id = Column(String(255), unique=True, nullable=True, index=True)
    email_date = Column(DateTime(timezone=True), nullable=True)
    
    # Contact information
    recruiter_name = Column(String(255), nullable=True)
    recruiter_email = Column(String(255), nullable=True)
    recruiter_phone = Column(String(50), nullable=True)
    
    # Metadata
    metadata = Column(JSON, default={})
    tags = Column(JSON, default=[])
    notes = Column(Text, nullable=True)
    
    # Priority and rating
    priority = Column(Integer, default=0)  # 0-5
    company_rating = Column(Float, nullable=True)  # 0-5
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="applications")
    emails = relationship("EmailLog", back_populates="application", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="application", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<JobApplication(company='{self.company_name}', role='{self.role_title}')>"


class EmailLog(Base):
    """Email log model"""
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("job_applications.id"), nullable=True)
    
    # Email details
    message_id = Column(String(255), unique=True, nullable=False, index=True)
    subject = Column(String(500), nullable=True)
    from_address = Column(String(255), nullable=True)
    to_address = Column(String(255), nullable=True)
    email_date = Column(DateTime(timezone=True), nullable=True)
    
    # Content
    body_text = Column(Text, nullable=True)
    body_html = Column(Text, nullable=True)
    
    # Classification
    is_job_related = Column(Boolean, default=False, index=True)
    classification = Column(Enum(EmailClassification), nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # Processing
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
    processing_time_ms = Column(Integer, nullable=True)
    
    # Metadata
    metadata = Column(JSON, default={})
    
    # Relationships
    application = relationship("JobApplication", back_populates="emails")
    
    def __repr__(self):
        return f"<EmailLog(message_id='{self.message_id}')>"


class Document(Base):
    """Document model for resumes, cover letters, etc."""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("job_applications.id"), nullable=False)
    
    # Document details
    document_type = Column(String(50), nullable=False)  # resume, cover_letter, portfolio, etc.
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=True)
    file_url = Column(String(500), nullable=False)  # S3/GCP URL
    mime_type = Column(String(100), nullable=True)
    
    # Version tracking
    version = Column(Integer, default=1)
    is_latest = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    application = relationship("JobApplication", back_populates="documents")
    
    def __repr__(self):
        return f"<Document(type='{self.document_type}', file='{self.file_name}')>"


class RefreshToken(Base):
    """Refresh token model for JWT authentication"""
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<RefreshToken(user_id={self.user_id})>"
