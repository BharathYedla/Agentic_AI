# 🚀 Backend API Implementation Guide

## Step-by-Step Guide to Add Real Job Data

This guide shows you **exactly how** to implement the backend APIs for LinkedIn, Google, and Indeed job integration.

---

## 📋 **Prerequisites**

1. **API Keys Needed:**
   - RapidAPI account (for LinkedIn Jobs)
   - SerpAPI account (for Google Jobs)
   - Indeed Publisher API account
   - Clearbit account (for company logos)
   - OpenAI account (for semantic matching)

2. **Python Packages:**
```bash
pip install requests serpapi openai PyPDF2 python-docx python-magic beautifulsoup4
```

---

## 🔧 **Step 1: Set Up API Keys**

### **1.1 Create `.env` file**

```bash
cd ios_app/backend
touch .env
```

### **1.2 Add API Keys to `.env`**

```bash
# .env file
RAPIDAPI_KEY=your_rapidapi_key_here
SERPAPI_KEY=your_serpapi_key_here
INDEED_PUBLISHER_ID=your_indeed_publisher_id_here
CLEARBIT_API_KEY=your_clearbit_key_here
OPENAI_API_KEY=your_openai_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost/jobtracker

# Redis
REDIS_URL=redis://localhost:6379
```

### **1.3 Update `config.py`**

```python
# backend/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Existing settings...
    
    # External API Keys
    RAPIDAPI_KEY: str
    SERPAPI_KEY: str
    INDEED_PUBLISHER_ID: str
    CLEARBIT_API_KEY: str
    OPENAI_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🔌 **Step 2: Implement LinkedIn Jobs Integration**

### **2.1 Create LinkedIn Service**

Create file: `backend/services/linkedin_service.py`

```python
"""
LinkedIn Jobs Integration using RapidAPI
"""
import requests
from typing import List, Optional
from datetime import datetime
from core.config import settings

class LinkedInJobsService:
    def __init__(self):
        self.api_url = "https://linkedin-data-api.p.rapidapi.com/search-jobs"
        self.headers = {
            "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
            "X-RapidAPI-Host": "linkedin-data-api.p.rapidapi.com"
        }
    
    def search_jobs(
        self,
        keywords: str,
        location: Optional[str] = None,
        experience_level: Optional[str] = None,
        limit: int = 20
    ) -> List[dict]:
        """
        Search LinkedIn jobs
        
        Args:
            keywords: Job search keywords (e.g., "iOS Developer")
            location: Location (e.g., "San Francisco, CA")
            experience_level: Experience level (entry, mid, senior)
            limit: Number of results
        
        Returns:
            List of job dictionaries
        """
        params = {
            "keywords": keywords,
            "locationId": self._get_location_id(location) if location else None,
            "datePosted": "anyTime",
            "sort": "mostRelevant"
        }
        
        # Add experience level filter
        if experience_level:
            params["experienceLevel"] = self._map_experience_level(experience_level)
        
        try:
            response = requests.get(
                self.api_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get("data", [])
            
            # Transform to our format
            return [self._transform_job(job) for job in jobs[:limit]]
            
        except Exception as e:
            print(f"LinkedIn API error: {e}")
            return []
    
    def _transform_job(self, job: dict) -> dict:
        """Transform LinkedIn job to our format"""
        return {
            "id": job.get("jobId", ""),
            "title": job.get("title", ""),
            "company": job.get("companyName", ""),
            "location": job.get("location", ""),
            "location_type": self._detect_location_type(job.get("workplaceType", "")),
            "description": job.get("description", ""),
            "salary": self._parse_salary(job.get("salary")),
            "posted_date": self._parse_date(job.get("listedAt")),
            "application_url": job.get("url", ""),
            "company_logo": job.get("companyLogo"),
            "experience_level": job.get("experienceLevel", "mid"),
            "employment_type": self._map_employment_type(job.get("employmentType")),
            "skills": [],  # Extract from description
            "requirements": [],  # Extract from description
            "benefits": [],  # Extract from description
            "is_remote": "remote" in job.get("workplaceType", "").lower(),
            "source": "linkedin"
        }
    
    def _get_location_id(self, location: str) -> str:
        """Map location string to LinkedIn location ID"""
        # LinkedIn location IDs (you'll need to build this mapping)
        location_map = {
            "san francisco": "102277331",
            "new york": "102571732",
            "seattle": "103644278",
            "remote": "0",
            # Add more as needed
        }
        return location_map.get(location.lower(), "0")
    
    def _map_experience_level(self, level: str) -> str:
        """Map our experience levels to LinkedIn's"""
        mapping = {
            "entry": "1",
            "mid": "2,3",
            "senior": "4,5",
            "lead": "5,6",
            "executive": "6"
        }
        return mapping.get(level, "2,3")
    
    def _detect_location_type(self, workplace_type: str) -> str:
        """Detect location type from workplace type"""
        workplace_type = workplace_type.lower()
        if "remote" in workplace_type:
            return "remote"
        elif "hybrid" in workplace_type:
            return "hybrid"
        else:
            return "onsite"
    
    def _parse_salary(self, salary_data: Optional[dict]) -> Optional[dict]:
        """Parse salary information"""
        if not salary_data:
            return None
        
        return {
            "min": salary_data.get("min", 0),
            "max": salary_data.get("max", 0),
            "currency": salary_data.get("currency", "USD"),
            "period": "year"
        }
    
    def _parse_date(self, timestamp: Optional[int]) -> str:
        """Parse LinkedIn timestamp to ISO date"""
        if not timestamp:
            return datetime.now().isoformat()
        
        return datetime.fromtimestamp(timestamp / 1000).isoformat()
    
    def _map_employment_type(self, emp_type: Optional[str]) -> str:
        """Map employment type"""
        if not emp_type:
            return "full_time"
        
        emp_type = emp_type.lower()
        if "full" in emp_type:
            return "full_time"
        elif "part" in emp_type:
            return "part_time"
        elif "contract" in emp_type:
            return "contract"
        else:
            return "full_time"
```

---

## 🔌 **Step 3: Implement Google Jobs Integration**

### **3.1 Create Google Jobs Service**

Create file: `backend/services/google_jobs_service.py`

```python
"""
Google Jobs Integration using SerpAPI
"""
from serpapi import GoogleSearch
from typing import List, Optional
from datetime import datetime
from core.config import settings

class GoogleJobsService:
    def __init__(self):
        self.api_key = settings.SERPAPI_KEY
    
    def search_jobs(
        self,
        query: str,
        location: Optional[str] = None,
        limit: int = 20
    ) -> List[dict]:
        """
        Search Google Jobs
        
        Args:
            query: Search query (e.g., "iOS Developer")
            location: Location (e.g., "San Francisco, CA")
            limit: Number of results
        
        Returns:
            List of job dictionaries
        """
        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location or "United States",
            "api_key": self.api_key,
            "num": limit
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            jobs = results.get("jobs_results", [])
            
            return [self._transform_job(job) for job in jobs[:limit]]
            
        except Exception as e:
            print(f"Google Jobs API error: {e}")
            return []
    
    def _transform_job(self, job: dict) -> dict:
        """Transform Google job to our format"""
        return {
            "id": job.get("job_id", ""),
            "title": job.get("title", ""),
            "company": job.get("company_name", ""),
            "location": job.get("location", ""),
            "location_type": self._detect_location_type(job.get("description", "")),
            "description": job.get("description", ""),
            "salary": self._parse_salary(job.get("detected_extensions")),
            "posted_date": self._parse_date(job.get("detected_extensions")),
            "application_url": job.get("apply_link", job.get("share_link", "")),
            "company_logo": None,  # Will fetch separately
            "experience_level": self._detect_experience_level(job.get("title", "")),
            "employment_type": self._detect_employment_type(job.get("detected_extensions")),
            "skills": [],
            "requirements": [],
            "benefits": [],
            "is_remote": self._is_remote(job.get("location", "")),
            "source": "google"
        }
    
    def _detect_location_type(self, description: str) -> str:
        """Detect if job is remote/hybrid/onsite"""
        description_lower = description.lower()
        if "remote" in description_lower:
            return "remote"
        elif "hybrid" in description_lower:
            return "hybrid"
        else:
            return "onsite"
    
    def _parse_salary(self, extensions: Optional[dict]) -> Optional[dict]:
        """Parse salary from extensions"""
        if not extensions:
            return None
        
        # Google Jobs provides salary in various formats
        # This is a simplified parser
        salary_text = extensions.get("salary", "")
        if not salary_text:
            return None
        
        # Parse salary range (e.g., "$100K - $150K a year")
        # You'll need more robust parsing here
        return None
    
    def _parse_date(self, extensions: Optional[dict]) -> str:
        """Parse posted date"""
        if not extensions:
            return datetime.now().isoformat()
        
        posted = extensions.get("posted_at", "")
        # Parse relative dates like "2 days ago"
        # For now, return current date
        return datetime.now().isoformat()
    
    def _detect_experience_level(self, title: str) -> str:
        """Detect experience level from title"""
        title_lower = title.lower()
        if "senior" in title_lower or "sr" in title_lower:
            return "senior"
        elif "junior" in title_lower or "jr" in title_lower:
            return "entry"
        elif "lead" in title_lower or "principal" in title_lower:
            return "lead"
        else:
            return "mid"
    
    def _detect_employment_type(self, extensions: Optional[dict]) -> str:
        """Detect employment type"""
        if not extensions:
            return "full_time"
        
        schedule = extensions.get("schedule_type", "").lower()
        if "part" in schedule:
            return "part_time"
        elif "contract" in schedule:
            return "contract"
        else:
            return "full_time"
    
    def _is_remote(self, location: str) -> bool:
        """Check if job is remote"""
        return "remote" in location.lower()
```

---

## 🔌 **Step 4: Implement Indeed Jobs Integration**

### **4.1 Create Indeed Service**

Create file: `backend/services/indeed_service.py`

```python
"""
Indeed Jobs Integration
"""
import requests
from typing import List, Optional
from datetime import datetime
from core.config import settings

class IndeedJobsService:
    def __init__(self):
        self.api_url = "http://api.indeed.com/ads/apisearch"
        self.publisher_id = settings.INDEED_PUBLISHER_ID
    
    def search_jobs(
        self,
        keywords: str,
        location: Optional[str] = None,
        limit: int = 20
    ) -> List[dict]:
        """
        Search Indeed jobs
        
        Args:
            keywords: Search keywords
            location: Location
            limit: Number of results
        
        Returns:
            List of job dictionaries
        """
        params = {
            "publisher": self.publisher_id,
            "q": keywords,
            "l": location or "",
            "sort": "relevance",
            "radius": "25",
            "st": "jobsite",
            "jt": "fulltime",
            "start": 0,
            "limit": limit,
            "fromage": "30",  # Last 30 days
            "format": "json",
            "v": "2"
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get("results", [])
            
            return [self._transform_job(job) for job in jobs]
            
        except Exception as e:
            print(f"Indeed API error: {e}")
            return []
    
    def _transform_job(self, job: dict) -> dict:
        """Transform Indeed job to our format"""
        return {
            "id": job.get("jobkey", ""),
            "title": job.get("jobtitle", ""),
            "company": job.get("company", ""),
            "location": f"{job.get('city', '')}, {job.get('state', '')}",
            "location_type": "onsite",  # Indeed doesn't always specify
            "description": job.get("snippet", ""),
            "salary": None,  # Not always provided
            "posted_date": job.get("date", datetime.now().isoformat()),
            "application_url": job.get("url", ""),
            "company_logo": None,
            "experience_level": "mid",
            "employment_type": "full_time",
            "skills": [],
            "requirements": [],
            "benefits": [],
            "is_remote": False,
            "source": "indeed"
        }
```

---

## 🔌 **Step 5: Implement Company Logo Fetching**

### **5.1 Create Logo Service**

Create file: `backend/services/logo_service.py`

```python
"""
Company Logo Fetching using Clearbit
"""
import requests
from typing import Optional
from core.config import settings

class LogoService:
    def __init__(self):
        self.clearbit_url = "https://logo.clearbit.com"
        self.api_key = settings.CLEARBIT_API_KEY
    
    def get_company_logo(
        self,
        company_name: str,
        domain: Optional[str] = None
    ) -> Optional[str]:
        """
        Get company logo URL
        
        Args:
            company_name: Company name
            domain: Company domain (e.g., "apple.com")
        
        Returns:
            Logo URL or None
        """
        # If domain provided, use it directly
        if domain:
            logo_url = f"{self.clearbit_url}/{domain}"
            if self._check_logo_exists(logo_url):
                return logo_url
        
        # Try to guess domain from company name
        guessed_domain = self._guess_domain(company_name)
        logo_url = f"{self.clearbit_url}/{guessed_domain}"
        
        if self._check_logo_exists(logo_url):
            return logo_url
        
        return None
    
    def _guess_domain(self, company_name: str) -> str:
        """Guess company domain from name"""
        # Remove common suffixes
        name = company_name.lower()
        name = name.replace(" inc", "").replace(" llc", "")
        name = name.replace(" corporation", "").replace(" corp", "")
        name = name.strip()
        
        # Replace spaces with nothing or dash
        domain = name.replace(" ", "")
        
        return f"{domain}.com"
    
    def _check_logo_exists(self, url: str) -> bool:
        """Check if logo URL is valid"""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False
```

---

## 📝 **Step 6: Create API Routes**

### **6.1 Create Jobs Router**

Create file: `backend/api/routes/jobs.py`

```python
"""
Job Recommendations API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from services.linkedin_service import LinkedInJobsService
from services.google_jobs_service import GoogleJobsService
from services.indeed_service import IndeedJobsService
from services.logo_service import LogoService
from models.database import User

router = APIRouter()

# Initialize services
linkedin_service = LinkedInJobsService()
google_service = GoogleJobsService()
indeed_service = IndeedJobsService()
logo_service = LogoService()


@router.get("/external/linkedin")
async def get_linkedin_jobs(
    keywords: str = Query(..., description="Search keywords"),
    location: Optional[str] = Query(None, description="Location"),
    experience_level: Optional[str] = Query(None),
    limit: int = Query(20, le=50),
    current_user: User = Depends(get_current_user)
):
    """Get jobs from LinkedIn"""
    jobs = linkedin_service.search_jobs(
        keywords=keywords,
        location=location,
        experience_level=experience_level,
        limit=limit
    )
    
    # Fetch company logos
    for job in jobs:
        if not job.get("company_logo"):
            job["company_logo"] = logo_service.get_company_logo(job["company"])
    
    return {
        "jobs": jobs,
        "total": len(jobs),
        "source": "linkedin"
    }


@router.get("/external/google")
async def get_google_jobs(
    query: str = Query(..., description="Search query"),
    location: Optional[str] = Query(None),
    limit: int = Query(20, le=50),
    current_user: User = Depends(get_current_user)
):
    """Get jobs from Google Jobs"""
    jobs = google_service.search_jobs(
        query=query,
        location=location,
        limit=limit
    )
    
    # Fetch company logos
    for job in jobs:
        job["company_logo"] = logo_service.get_company_logo(job["company"])
    
    return {
        "jobs": jobs,
        "total": len(jobs),
        "source": "google"
    }


@router.get("/external/indeed")
async def get_indeed_jobs(
    keywords: str = Query(...),
    location: Optional[str] = Query(None),
    limit: int = Query(20, le=50),
    current_user: User = Depends(get_current_user)
):
    """Get jobs from Indeed"""
    jobs = indeed_service.search_jobs(
        keywords=keywords,
        location=location,
        limit=limit
    )
    
    # Fetch company logos
    for job in jobs:
        job["company_logo"] = logo_service.get_company_logo(job["company"])
    
    return {
        "jobs": jobs,
        "total": len(jobs),
        "source": "indeed"
    }


@router.get("/external/aggregate")
async def get_aggregated_jobs(
    keywords: str = Query(...),
    location: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    current_user: User = Depends(get_current_user)
):
    """Get jobs from all sources"""
    all_jobs = []
    
    # Fetch from LinkedIn
    linkedin_jobs = linkedin_service.search_jobs(
        keywords=keywords,
        location=location,
        experience_level=experience_level,
        limit=limit // 3
    )
    all_jobs.extend(linkedin_jobs)
    
    # Fetch from Google
    google_jobs = google_service.search_jobs(
        query=keywords,
        location=location,
        limit=limit // 3
    )
    all_jobs.extend(google_jobs)
    
    # Fetch from Indeed
    indeed_jobs = indeed_service.search_jobs(
        keywords=keywords,
        location=location,
        limit=limit // 3
    )
    all_jobs.extend(indeed_jobs)
    
    # Fetch logos for all
    for job in all_jobs:
        if not job.get("company_logo"):
            job["company_logo"] = logo_service.get_company_logo(job["company"])
    
    # Remove duplicates based on title + company
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = (job["title"].lower(), job["company"].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    return {
        "jobs": unique_jobs[:limit],
        "total": len(unique_jobs),
        "source": "aggregated"
    }


@router.get("/company-logo")
async def get_company_logo(
    company_name: str = Query(...),
    domain: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """Get company logo URL"""
    logo_url = logo_service.get_company_logo(company_name, domain)
    
    return {
        "logo_url": logo_url
    }
```

---

## 📝 **Step 7: Register Routes in Main App**

### **7.1 Update `main.py`**

```python
# backend/main.py

# Add this import
from api.routes import jobs

# Add this line with other router includes
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
```

---

## 🧪 **Step 8: Test the APIs**

### **8.1 Start the Backend**

```bash
cd ios_app/backend
source venv/bin/activate
uvicorn main:app --reload
```

### **8.2 Test with cURL**

```bash
# Test LinkedIn jobs
curl -X GET "http://localhost:8000/api/v1/jobs/external/linkedin?keywords=iOS%20Developer&location=San%20Francisco" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Test Google jobs
curl -X GET "http://localhost:8000/api/v1/jobs/external/google?query=iOS%20Developer&location=San%20Francisco" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Test aggregated
curl -X GET "http://localhost:8000/api/v1/jobs/external/aggregate?keywords=iOS%20Developer&location=San%20Francisco" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## ✅ **Step 9: Verify in iOS App**

1. **Build and run** the iOS app
2. **Sign in** to get authenticated
3. **Navigate to Jobs tab**
4. **Jobs should now load** from real APIs!

---

## 🎉 **Done!**

You now have:
- ✅ LinkedIn Jobs integration
- ✅ Google Jobs integration
- ✅ Indeed Jobs integration
- ✅ Company logo fetching
- ✅ Aggregated search
- ✅ Working iOS app!

**Next:** Implement semantic matching with OpenAI (see next guide)
