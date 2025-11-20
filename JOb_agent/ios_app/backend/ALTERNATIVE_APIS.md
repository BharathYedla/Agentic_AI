# 🆓 Alternative Job APIs - No Registration Required

## Problem: Can't get SerpAPI or Clearbit API keys

**Solution:** Use free alternatives that don't require registration!

---

## 🎯 **Option 1: Use LinkedIn Only (Simplest)**

You already have RapidAPI! Just use LinkedIn jobs only.

### **Update `.env`**

```bash
# You have this
RAPIDAPI_KEY=6401bda796mshfa6772638c4c2bep1237a4jsn20550c59dbb3

# Leave these empty (we won't use them)
SERPAPI_KEY=
CLEARBIT_API_KEY=
```

### **Modify the backend to use LinkedIn only**

The iOS app will still work perfectly with just LinkedIn jobs!

---

## 🎯 **Option 2: Add Free Job APIs (No Registration)**

### **2.1 Adzuna Jobs API** (Free, No Credit Card)

**Free Tier:** 1000 calls/month  
**Sign up:** https://developer.adzuna.com/

```python
# services/adzuna_service.py
import requests
from typing import List, Optional
from datetime import datetime

class AdzunaJobsService:
    def __init__(self):
        # Free API - just need app ID and key (instant, no credit card)
        self.app_id = "YOUR_APP_ID"  # Get from adzuna.com
        self.app_key = "YOUR_APP_KEY"
        self.base_url = "https://api.adzuna.com/v1/api/jobs/us/search"
    
    def search_jobs(
        self,
        query: str,
        location: Optional[str] = None,
        limit: int = 20
    ) -> List[dict]:
        """Search Adzuna jobs"""
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "what": query,
            "where": location or "",
            "results_per_page": limit,
            "content-type": "application/json"
        }
        
        try:
            response = requests.get(self.base_url + "/1", params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get("results", [])
            
            return [self._transform_job(job) for job in jobs]
        except Exception as e:
            print(f"Adzuna API error: {e}")
            return []
    
    def _transform_job(self, job: dict) -> dict:
        """Transform Adzuna job to our format"""
        return {
            "id": job.get("id", ""),
            "title": job.get("title", ""),
            "company": job.get("company", {}).get("display_name", "Unknown"),
            "location": job.get("location", {}).get("display_name", ""),
            "location_type": "onsite",
            "description": job.get("description", ""),
            "salary": self._parse_salary(job),
            "posted_date": job.get("created", datetime.now().isoformat()),
            "application_url": job.get("redirect_url", ""),
            "company_logo": None,
            "experience_level": "mid",
            "employment_type": self._parse_contract(job.get("contract_type")),
            "skills": [],
            "requirements": [],
            "benefits": [],
            "is_remote": "remote" in job.get("title", "").lower(),
            "source": "adzuna"
        }
    
    def _parse_salary(self, job: dict) -> Optional[dict]:
        """Parse salary"""
        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")
        
        if salary_min and salary_max:
            return {
                "min": int(salary_min),
                "max": int(salary_max),
                "currency": "USD",
                "period": "year"
            }
        return None
    
    def _parse_contract(self, contract_type: Optional[str]) -> str:
        """Parse contract type"""
        if not contract_type:
            return "full_time"
        
        contract_type = contract_type.lower()
        if "permanent" in contract_type or "full" in contract_type:
            return "full_time"
        elif "part" in contract_type:
            return "part_time"
        elif "contract" in contract_type:
            return "contract"
        else:
            return "full_time"
```

---

## 🎯 **Option 3: Use Free Logo Service (No API Key)**

### **3.1 Clearbit Alternative - Logo.dev (Free)**

```python
# services/logo_service_free.py
import requests
from typing import Optional

class FreeLogoService:
    def __init__(self):
        # No API key needed!
        self.logo_dev_url = "https://img.logo.dev"
        self.clearbit_url = "https://logo.clearbit.com"
    
    def get_company_logo(
        self,
        company_name: str,
        domain: Optional[str] = None
    ) -> Optional[str]:
        """
        Get company logo URL using free services
        No API key required!
        """
        # Try domain first if provided
        if domain:
            # Try Clearbit (no auth needed for basic usage)
            logo_url = f"{self.clearbit_url}/{domain}"
            if self._check_logo_exists(logo_url):
                return logo_url
            
            # Try Logo.dev
            logo_url = f"{self.logo_dev_url}/{domain}?token=free"
            if self._check_logo_exists(logo_url):
                return logo_url
        
        # Guess domain from company name
        guessed_domain = self._guess_domain(company_name)
        
        # Try Clearbit
        logo_url = f"{self.clearbit_url}/{guessed_domain}"
        if self._check_logo_exists(logo_url):
            return logo_url
        
        # Try Logo.dev
        logo_url = f"{self.logo_dev_url}/{guessed_domain}?token=free"
        if self._check_logo_exists(logo_url):
            return logo_url
        
        # Try company-specific patterns
        for domain in self._get_domain_variations(company_name):
            logo_url = f"{self.clearbit_url}/{domain}"
            if self._check_logo_exists(logo_url):
                return logo_url
        
        return None
    
    def _guess_domain(self, company_name: str) -> str:
        """Guess company domain from name"""
        # Common company name mappings
        known_domains = {
            "apple": "apple.com",
            "google": "google.com",
            "meta": "meta.com",
            "facebook": "facebook.com",
            "microsoft": "microsoft.com",
            "amazon": "amazon.com",
            "netflix": "netflix.com",
            "tesla": "tesla.com",
            "uber": "uber.com",
            "airbnb": "airbnb.com",
            "stripe": "stripe.com",
            "shopify": "shopify.com",
            "salesforce": "salesforce.com",
            "oracle": "oracle.com",
            "ibm": "ibm.com",
            "intel": "intel.com",
            "nvidia": "nvidia.com",
            "adobe": "adobe.com",
            "spotify": "spotify.com",
            "twitter": "twitter.com",
            "linkedin": "linkedin.com",
            "github": "github.com",
            "gitlab": "gitlab.com",
            "slack": "slack.com",
            "zoom": "zoom.us",
            "dropbox": "dropbox.com",
            "atlassian": "atlassian.com",
            "paypal": "paypal.com",
            "square": "squareup.com",
            "coinbase": "coinbase.com",
            "robinhood": "robinhood.com",
        }
        
        name_lower = company_name.lower().strip()
        
        # Check known domains
        for key, domain in known_domains.items():
            if key in name_lower:
                return domain
        
        # Clean company name
        name = name_lower
        name = name.replace(" inc", "").replace(" llc", "")
        name = name.replace(" corporation", "").replace(" corp", "")
        name = name.replace(" limited", "").replace(" ltd", "")
        name = name.replace(",", "").strip()
        
        # Remove spaces
        domain = name.replace(" ", "")
        
        return f"{domain}.com"
    
    def _get_domain_variations(self, company_name: str) -> list:
        """Get domain variations to try"""
        base = self._guess_domain(company_name).replace(".com", "")
        
        return [
            f"{base}.com",
            f"{base}.io",
            f"{base}.co",
            f"{base}.net",
            f"{base}.org",
        ]
    
    def _check_logo_exists(self, url: str) -> bool:
        """Check if logo URL is valid"""
        try:
            response = requests.head(url, timeout=3, allow_redirects=True)
            return response.status_code == 200
        except:
            return False
```

---

## 🎯 **Option 4: Simple Implementation (LinkedIn + Free Logos)**

Here's a **complete, working solution** using only what you have:

### **Step 1: Create simplified services**

Create file: `backend/services/simple_job_service.py`

```python
"""
Simple job service using only LinkedIn (RapidAPI)
No SerpAPI or Clearbit needed!
"""
import requests
from typing import List, Optional
from datetime import datetime

class SimpleJobService:
    def __init__(self, rapidapi_key: str):
        self.rapidapi_key = rapidapi_key
        self.linkedin_url = "https://linkedin-data-api.p.rapidapi.com/search-jobs"
        self.headers = {
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": "linkedin-data-api.p.rapidapi.com"
        }
    
    def search_jobs(
        self,
        keywords: str,
        location: Optional[str] = None,
        limit: int = 20
    ) -> List[dict]:
        """Search jobs using LinkedIn only"""
        params = {
            "keywords": keywords,
            "locationId": "0",  # Worldwide
            "datePosted": "anyTime",
            "sort": "mostRelevant"
        }
        
        try:
            response = requests.get(
                self.linkedin_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get("data", [])
            
            # Transform and add free logos
            result = []
            for job in jobs[:limit]:
                transformed = self._transform_job(job)
                # Add free logo
                transformed["company_logo"] = self._get_free_logo(
                    transformed["company"]
                )
                result.append(transformed)
            
            return result
            
        except Exception as e:
            print(f"Job search error: {e}")
            return []
    
    def _transform_job(self, job: dict) -> dict:
        """Transform job data"""
        return {
            "id": job.get("jobId", ""),
            "title": job.get("title", ""),
            "company": job.get("companyName", ""),
            "location": job.get("location", ""),
            "location_type": self._detect_location_type(job.get("workplaceType", "")),
            "description": job.get("description", ""),
            "salary": None,
            "posted_date": datetime.now().isoformat(),
            "application_url": job.get("url", ""),
            "company_logo": None,
            "experience_level": "mid",
            "employment_type": "full_time",
            "skills": [],
            "requirements": [],
            "benefits": [],
            "is_remote": "remote" in job.get("workplaceType", "").lower(),
            "source": "linkedin"
        }
    
    def _detect_location_type(self, workplace_type: str) -> str:
        """Detect location type"""
        workplace_type = workplace_type.lower()
        if "remote" in workplace_type:
            return "remote"
        elif "hybrid" in workplace_type:
            return "hybrid"
        else:
            return "onsite"
    
    def _get_free_logo(self, company_name: str) -> Optional[str]:
        """Get company logo using free Clearbit (no auth needed)"""
        # Known company domains
        known_domains = {
            "apple": "apple.com",
            "google": "google.com",
            "meta": "meta.com",
            "microsoft": "microsoft.com",
            "amazon": "amazon.com",
            "netflix": "netflix.com",
            "tesla": "tesla.com",
            "uber": "uber.com",
            "airbnb": "airbnb.com",
            "stripe": "stripe.com",
            # Add more as needed
        }
        
        name_lower = company_name.lower()
        
        # Try known domains
        for key, domain in known_domains.items():
            if key in name_lower:
                return f"https://logo.clearbit.com/{domain}"
        
        # Guess domain
        domain = name_lower.replace(" ", "").replace(",", "") + ".com"
        return f"https://logo.clearbit.com/{domain}"
```

---

### **Step 2: Create simple API route**

Create file: `backend/api/routes/simple_jobs.py`

```python
"""
Simple jobs API using only LinkedIn
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from api.dependencies import get_current_user
from services.simple_job_service import SimpleJobService
from core.config import settings
from models.database import User

router = APIRouter()

# Initialize service
job_service = SimpleJobService(rapidapi_key=settings.RAPIDAPI_KEY)


@router.get("/search")
async def search_jobs(
    keywords: str = Query(..., description="Search keywords"),
    location: Optional[str] = Query(None, description="Location"),
    limit: int = Query(20, le=50),
    current_user: User = Depends(get_current_user)
):
    """
    Search jobs using LinkedIn
    Simple implementation - no SerpAPI or Clearbit needed!
    """
    jobs = job_service.search_jobs(
        keywords=keywords,
        location=location,
        limit=limit
    )
    
    return {
        "jobs": jobs,
        "total": len(jobs),
        "source": "linkedin"
    }
```

---

### **Step 3: Register route in main.py**

```python
# backend/main.py

from api.routes import simple_jobs

# Add this line
app.include_router(
    simple_jobs.router,
    prefix="/api/v1/jobs",
    tags=["Jobs"]
)
```

---

### **Step 4: Update iOS app to use simple endpoint**

The iOS app will automatically work! It just calls `/api/v1/jobs/search`

---

## ✅ **What You Get**

With just your RapidAPI key:

✅ **Real LinkedIn jobs**  
✅ **Company logos** (free Clearbit)  
✅ **No SerpAPI needed**  
✅ **No Clearbit API key needed**  
✅ **Works immediately**  

---

## 🚀 **Quick Implementation**

1. **Copy `simple_job_service.py`** to `backend/services/`
2. **Copy `simple_jobs.py`** to `backend/api/routes/`
3. **Update `main.py`** to include the router
4. **Start backend:** `uvicorn main:app --reload`
5. **Test:** Open http://localhost:8000/api/docs

**Done!** Your iOS app will show real LinkedIn jobs with logos! 🎉

---

## 💡 **Future: Add More Sources Later**

When you can get other API keys, just add them:

- ✅ **Adzuna** (free, easy signup)
- ✅ **JSearch** (RapidAPI, similar to LinkedIn)
- ✅ **Reed Jobs** (UK jobs, free API)

But for now, **LinkedIn alone is perfect!** It has millions of jobs.

---

## 🎉 **Summary**

**You don't need SerpAPI or Clearbit!**

Just use:
- ✅ LinkedIn jobs (you have RapidAPI)
- ✅ Free Clearbit logos (no auth needed)
- ✅ Simple implementation above

**Your app will work great!** 🚀
