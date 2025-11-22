from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    IN_PROGRESS = "in_progress"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    OFFER_RECEIVED = "offer_received"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class ApplicationBase(BaseModel):
    company_name: str
    role_title: str
    status: ApplicationStatus = ApplicationStatus.APPLIED
    job_description: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    application_url: Optional[str] = None
    company_website: Optional[str] = None
    notes: Optional[str] = None
    priority: int = Field(default=0, ge=0, le=5)

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    role_title: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    job_description: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    application_url: Optional[str] = None
    company_website: Optional[str] = None
    notes: Optional[str] = None
    priority: Optional[int] = Field(None, ge=0, le=5)

class ApplicationResponse(ApplicationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class JobSearchResponse(BaseModel):
    id: str
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    posted_at: Optional[str] = None
    source: str = "linkedin"
    match_score: Optional[int] = None

class DashboardStats(BaseModel):
    total_applications: int
    interviews: int
    offers: int
    response_rate: float
    recent_activity: List[ApplicationResponse]
