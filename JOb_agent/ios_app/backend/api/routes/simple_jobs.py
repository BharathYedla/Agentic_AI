"""
Simple Jobs API Routes
Using only LinkedIn (RapidAPI) - No SerpAPI or Clearbit needed!
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from services.simple_job_service import SimpleJobService

router = APIRouter()

# Initialize service
try:
    job_service = SimpleJobService()
except ValueError as e:
    print(f"Warning: {e}")
    job_service = None


@router.get("/search")
async def search_jobs(
    keywords: str = Query("iOS Developer", description="Search keywords"),
    location: Optional[str] = Query(None, description="Location"),
    experience_level: Optional[str] = Query(None, description="Experience level"),
    limit: int = Query(20, le=50, description="Number of results")
):
    """
    Search jobs using LinkedIn
    
    Simple implementation - only needs RapidAPI key!
    No SerpAPI or Clearbit API key required.
    """
    if not job_service:
        raise HTTPException(
            status_code=500,
            detail="Job service not initialized. Check RAPIDAPI_KEY in .env"
        )
    
    try:
        jobs = job_service.search_jobs(
            keywords=keywords,
            location=location,
            experience_level=experience_level,
            limit=limit
        )
        
        return {
            "jobs": jobs,
            "total": len(jobs),
            "source": "linkedin"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching jobs: {str(e)}"
        )


@router.get("/external/linkedin")
async def get_linkedin_jobs(
    keywords: str = Query(..., description="Search keywords"),
    location: Optional[str] = Query(None, description="Location"),
    experience_level: Optional[str] = Query(None),
    limit: int = Query(20, le=50)
):
    """Get jobs from LinkedIn"""
    return await search_jobs(keywords, location, experience_level, limit)


@router.get("/external/aggregate")
async def get_aggregated_jobs(
    keywords: str = Query(..., description="Search keywords"),
    location: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    limit: int = Query(50, le=100)
):
    """
    Get aggregated jobs
    Currently only LinkedIn, but can add more sources later
    """
    return await search_jobs(keywords, location, experience_level, limit)


@router.get("/recommendations")
async def get_recommendations(
    query: Optional[str] = Query(None, description="Search query"),
    location: Optional[str] = Query(None, description="Location"),
    use_semantic_search: bool = Query(True),
    limit: int = Query(20, le=50),
    offset: int = Query(0)
):
    """
    Get job recommendations
    Uses LinkedIn jobs with optional semantic matching
    """
    keywords = query or "iOS Developer"
    return await search_jobs(keywords, location, None, limit)


@router.get("/company-logo")
async def get_company_logo(
    company_name: str = Query(..., description="Company name"),
    domain: Optional[str] = Query(None, description="Company domain")
):
    """
    Get company logo URL
    Uses free Clearbit service (no API key needed)
    """
    if not job_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    logo_url = job_service._get_free_logo(company_name)
    
    return {
        "logo_url": logo_url
    }


@router.post("/{job_id}/save")
async def save_job(job_id: str):
    """Save a job (placeholder - implement with database)"""
    return {"message": "Job saved", "job_id": job_id}


@router.delete("/{job_id}/save")
async def unsave_job(job_id: str):
    """Unsave a job (placeholder - implement with database)"""
    return {"message": "Job unsaved", "job_id": job_id}


@router.get("/saved")
async def get_saved_jobs():
    """Get saved jobs (placeholder - implement with database)"""
    return {"jobs": [], "total": 0}
