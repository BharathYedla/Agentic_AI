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
    Fallback to mock data if API key is missing.
    """
    if not job_service:
        # Return mock data if service is not available
        return {
            "jobs": _get_mock_jobs(keywords, location),
            "total": 4,
            "source": "mock"
        }
    
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
        print(f"Error fetching jobs: {e}")
        # Fallback to mock data on error
        return {
            "jobs": _get_mock_jobs(keywords, location),
            "total": 4,
            "source": "mock_fallback"
        }

def _get_mock_jobs(keywords: str, location: Optional[str]):
    return [
        {
            "id": "1",
            "title": f"Senior {keywords}",
            "company": "TechCorp Inc.",
            "location": location or "San Francisco, CA",
            "description": "We are looking for an experienced developer...",
            "url": "https://example.com",
            "posted_at": "2023-10-01T10:00:00Z",
            "source": "mock",
            "match_score": 95,
            "company_logo": "https://logo.clearbit.com/google.com"
        },
        {
            "id": "2",
            "title": "AI Research Scientist",
            "company": "DeepMind",
            "location": "London, UK",
            "description": "Join our research team...",
            "url": "https://deepmind.com",
            "posted_at": "2023-10-02T11:00:00Z",
            "source": "mock",
            "match_score": 92,
            "company_logo": "https://logo.clearbit.com/deepmind.com"
        },
        {
            "id": "3",
            "title": "Product Designer",
            "company": "Creative Studio",
            "location": "New York, NY",
            "description": "Design beautiful interfaces...",
            "url": "https://example.com",
            "posted_at": "2023-10-03T12:00:00Z",
            "source": "mock",
            "match_score": 88,
            "company_logo": "https://logo.clearbit.com/airbnb.com"
        },
        {
            "id": "4",
            "title": "Full Stack Developer",
            "company": "StartupX",
            "location": "Remote",
            "description": "Build the future...",
            "url": "https://example.com",
            "posted_at": "2023-10-04T13:00:00Z",
            "source": "mock",
            "match_score": 85,
            "company_logo": "https://logo.clearbit.com/stripe.com"
        }
    ]


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


@router.get("/{job_id}")
async def get_job_details(job_id: str):
    """
    Get job details by ID
    For now, returns mock data or searches if possible
    """
    # Check mock data first
    mock_jobs = _get_mock_jobs("iOS Developer", "San Francisco, CA")
    for job in mock_jobs:
        if job["id"] == job_id:
            return job
            
    # If not in mock, return a generic mock for testing UI
    return {
        "id": job_id,
        "title": "Senior Software Engineer",
        "company": "Tech Giant Corp",
        "location": "San Francisco, CA",
        "description": "This is a detailed description of the job. We are looking for a talented engineer to join our team. You will be working on cutting-edge technologies and solving complex problems.\n\nResponsibilities:\n- Design and build scalable systems\n- Collaborate with cross-functional teams\n- Write clean, maintainable code\n\nRequirements:\n- 5+ years of experience\n- Proficiency in Python and React\n- Strong problem-solving skills",
        "url": "https://example.com",
        "posted_at": "2023-10-05T10:00:00Z",
        "source": "mock_detail",
        "match_score": 88,
        "company_logo": "https://logo.clearbit.com/google.com",
        "skills": ["Python", "React", "AWS", "System Design"],
        "benefits": ["Competitive Salary", "Health Insurance", "Remote Work", "Stock Options"]
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
