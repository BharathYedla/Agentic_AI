from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from core.database import get_db
from models.database import JobApplication, ApplicationStatus
from api.schemas import DashboardStats, ApplicationResponse

router = APIRouter()

async def get_current_user_id():
    return 1

@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get dashboard statistics"""
    
    # Total applications
    total_query = select(func.count(JobApplication.id)).where(JobApplication.user_id == user_id)
    total_result = await db.execute(total_query)
    total_applications = total_result.scalar() or 0
    
    # Interviews
    interview_query = select(func.count(JobApplication.id)).where(
        JobApplication.user_id == user_id,
        JobApplication.status.in_([
            ApplicationStatus.INTERVIEW_SCHEDULED,
            ApplicationStatus.INTERVIEW_COMPLETED
        ])
    )
    interview_result = await db.execute(interview_query)
    interviews = interview_result.scalar() or 0
    
    # Offers
    offer_query = select(func.count(JobApplication.id)).where(
        JobApplication.user_id == user_id,
        JobApplication.status.in_([
            ApplicationStatus.OFFER_RECEIVED,
            ApplicationStatus.OFFER_ACCEPTED,
            ApplicationStatus.OFFER_DECLINED
        ])
    )
    offer_result = await db.execute(offer_query)
    offers = offer_result.scalar() or 0
    
    # Response Rate (Interviews + Offers + Rejections) / Total
    responded_query = select(func.count(JobApplication.id)).where(
        JobApplication.user_id == user_id,
        JobApplication.status.notin_([
            ApplicationStatus.APPLIED,
            ApplicationStatus.WITHDRAWN
        ])
    )
    responded_result = await db.execute(responded_query)
    responded_count = responded_result.scalar() or 0
    
    response_rate = (responded_count / total_applications * 100) if total_applications > 0 else 0.0
    
    # Recent Activity (Last 5 updated applications)
    recent_query = select(JobApplication).where(
        JobApplication.user_id == user_id
    ).order_by(desc(JobApplication.updated_at)).limit(5)
    
    recent_result = await db.execute(recent_query)
    recent_activity = recent_result.scalars().all()
    
    return {
        "total_applications": total_applications,
        "interviews": interviews,
        "offers": offers,
        "response_rate": round(response_rate, 1),
        "recent_activity": recent_activity
    }
