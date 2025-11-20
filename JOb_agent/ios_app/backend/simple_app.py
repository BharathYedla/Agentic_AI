"""
Simplified FastAPI app for testing jobs API
No database or complex dependencies required
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import our job service
from services.simple_job_service import SimpleJobService

# Create app
app = FastAPI(
    title="JobTracker Jobs API",
    description="Simple jobs API using JSearch",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize job service
job_service = SimpleJobService()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "JobTracker Jobs API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


@app.get("/api/v1/jobs/search")
async def search_jobs(
    keywords: str = Query("iOS Developer", description="Search keywords"),
    location: Optional[str] = Query(None, description="Location"),
    experience_level: Optional[str] = Query(None, description="Experience level"),
    limit: int = Query(20, le=50)
):
    """Search jobs"""
    jobs = job_service.search_jobs(
        keywords=keywords,
        location=location,
        experience_level=experience_level,
        limit=limit
    )
    
    return {
        "jobs": jobs,
        "total": len(jobs),
        "source": "jsearch"
    }


@app.get("/api/v1/jobs/external/linkedin")
async def get_linkedin_jobs(
    keywords: str = Query(...),
    location: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    limit: int = Query(20, le=50)
):
    """Get jobs (via JSearch)"""
    return await search_jobs(keywords, location, experience_level, limit)


@app.get("/api/v1/jobs/external/aggregate")
async def get_aggregated_jobs(
    keywords: str = Query(...),
    location: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    limit: int = Query(50, le=100)
):
    """Get aggregated jobs"""
    return await search_jobs(keywords, location, experience_level, limit)


@app.get("/api/v1/jobs/recommendations")
async def get_recommendations(
    query: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    limit: int = Query(20, le=50)
):
    """Get job recommendations"""
    keywords = query or "iOS Developer"
    return await search_jobs(keywords, location, None, limit)


@app.get("/api/v1/jobs/company-logo")
async def get_company_logo(
    company_name: str = Query(...),
    domain: Optional[str] = Query(None)
):
    """Get company logo URL"""
    logo_url = job_service._get_free_logo(company_name)
    return {"logo_url": logo_url}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
