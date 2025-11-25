from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from core.database import get_db
from models.database import JobApplication, User
from api.schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate, ApplicationStatus

router = APIRouter()

# TODO: Get current user from auth token. For now, we'll use a hardcoded user_id=1
# You should implement a proper get_current_user dependency
async def get_current_user_id():
    return 1

@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    skip: int = 0,
    limit: int = 100,
    status: ApplicationStatus = None,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get all applications for the current user"""
    query = select(JobApplication).where(JobApplication.user_id == user_id)
    
    if status:
        query = query.where(JobApplication.status == status)
        
    query = query.order_by(desc(JobApplication.updated_at)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    application: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Create a new job application"""
    db_application = JobApplication(**application.model_dump(), user_id=user_id)
    db.add(db_application)
    await db.commit()
    await db.refresh(db_application)
    return db_application

@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get a specific application"""
    query = select(JobApplication).where(
        JobApplication.id == application_id,
        JobApplication.user_id == user_id
    )
    result = await db.execute(query)
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    return application

@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Update an application"""
    query = select(JobApplication).where(
        JobApplication.id == application_id,
        JobApplication.user_id == user_id
    )
    result = await db.execute(query)
    db_application = result.scalar_one_or_none()
    
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    update_data = application_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_application, key, value)
        
    await db.commit()
    await db.refresh(db_application)
    return db_application

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Delete an application"""
    query = select(JobApplication).where(
        JobApplication.id == application_id,
        JobApplication.user_id == user_id
    )
    result = await db.execute(query)
    db_application = result.scalar_one_or_none()
    
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    await db.delete(db_application)
    await db.commit()
    return None
