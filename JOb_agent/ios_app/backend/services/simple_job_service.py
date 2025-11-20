"""
Job Service using JSearch API (RapidAPI)
JSearch aggregates jobs from LinkedIn, Indeed, Glassdoor, and more!
"""
import requests
from typing import List, Optional
from datetime import datetime
import os

class SimpleJobService:
    def __init__(self):
        self.rapidapi_key = os.getenv("RAPIDAPI_KEY")
        if not self.rapidapi_key:
            raise ValueError("RAPIDAPI_KEY not found in environment variables")
        
        # JSearch API (aggregates from LinkedIn, Indeed, Glassdoor, etc.)
        self.jsearch_url = "https://jsearch.p.rapidapi.com/search"
        self.headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        # Known company domains for logo fetching
        self.known_domains = {
            "apple": "apple.com",
            "google": "google.com",
            "alphabet": "google.com",
            "meta": "meta.com",
            "facebook": "facebook.com",
            "microsoft": "microsoft.com",
            "amazon": "amazon.com",
            "netflix": "netflix.com",
            "tesla": "tesla.com",
            "uber": "uber.com",
            "lyft": "lyft.com",
            "airbnb": "airbnb.com",
            "stripe": "stripe.com",
            "shopify": "shopify.com",
            "salesforce": "salesforce.com",
            "oracle": "oracle.com",
            "ibm": "ibm.com",
            "intel": "intel.com",
            "nvidia": "nvidia.com",
            "amd": "amd.com",
            "adobe": "adobe.com",
            "spotify": "spotify.com",
            "twitter": "twitter.com",
            "x corp": "x.com",
            "linkedin": "linkedin.com",
            "github": "github.com",
            "gitlab": "gitlab.com",
            "slack": "slack.com",
            "zoom": "zoom.us",
            "dropbox": "dropbox.com",
            "atlassian": "atlassian.com",
            "paypal": "paypal.com",
            "square": "squareup.com",
            "block": "block.xyz",
            "coinbase": "coinbase.com",
            "robinhood": "robinhood.com",
        }
    
    def search_jobs(
        self,
        keywords: str,
        location: Optional[str] = None,
        experience_level: Optional[str] = None,
        limit: int = 20
    ) -> List[dict]:
        """
        Search jobs using JSearch API
        Aggregates from LinkedIn, Indeed, Glassdoor, and more!
        
        Args:
            keywords: Job search keywords (e.g., "iOS Developer")
            location: Location (e.g., "San Francisco, CA")
            experience_level: Experience level (entry, mid, senior)
            limit: Number of results
        
        Returns:
            List of job dictionaries
        """
        # Build query
        query = keywords
        if location:
            query += f" in {location}"
        
        params = {
            "query": query,
            "num_pages": "1",
            "page": "1"
        }
        
        # Add date filter for recent jobs
        params["date_posted"] = "month"  # Last month
        
        # Add employment type
        if experience_level:
            # JSearch doesn't have direct experience level filter
            # We'll filter in post-processing
            pass
        
        try:
            print(f"Searching JSearch: {query}")
            response = requests.get(
                self.jsearch_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get("data", [])
            
            print(f"Found {len(jobs)} jobs from JSearch")
            
            # Transform and add logos
            result = []
            for job in jobs[:limit]:
                transformed = self._transform_job(job)
                # Add free logo
                if not transformed.get("company_logo"):
                    transformed["company_logo"] = self._get_free_logo(
                        transformed["company"]
                    )
                # Add match score (placeholder)
                transformed["match_score"] = 0.0
                transformed["match_reasons"] = []
                transformed["is_saved"] = False
                
                result.append(transformed)
            
            return result
            
        except Exception as e:
            print(f"JSearch API error: {e}")
            return []
    
    def _transform_job(self, job: dict) -> dict:
        """Transform JSearch job to our format"""
        # JSearch provides rich data
        employer_logo = job.get("employer_logo")
        
        return {
            "id": str(job.get("job_id", "")),
            "title": job.get("job_title", ""),
            "company": job.get("employer_name", ""),
            "location": self._format_location(job),
            "location_type": self._detect_location_type(job),
            "description": job.get("job_description", ""),
            "salary": self._parse_salary(job),
            "posted_date": self._parse_date(job.get("job_posted_at_datetime_utc")),
            "application_url": job.get("job_apply_link", job.get("job_google_link", "")),
            "company_logo": employer_logo,  # JSearch provides logos!
            "experience_level": self._detect_experience_level(job),
            "employment_type": self._map_employment_type(job.get("job_employment_type")),
            "skills": job.get("job_required_skills", []),
            "requirements": self._extract_requirements(job.get("job_highlights", {})),
            "benefits": self._extract_benefits(job.get("job_highlights", {})),
            "is_remote": job.get("job_is_remote", False),
            "source": "jsearch"  # Aggregates from multiple sources
        }
    
    def _format_location(self, job: dict) -> str:
        """Format location from job data"""
        city = job.get("job_city", "")
        state = job.get("job_state", "")
        country = job.get("job_country", "")
        
        parts = [p for p in [city, state] if p]
        if not parts and country:
            return country
        return ", ".join(parts) if parts else "Remote"
    
    def _detect_location_type(self, job: dict) -> str:
        """Detect location type"""
        if job.get("job_is_remote", False):
            return "remote"
        
        # Check description for hybrid
        desc = job.get("job_description", "").lower()
        if "hybrid" in desc:
            return "hybrid"
        
        return "onsite"
    
    def _detect_experience_level(self, job: dict) -> str:
        """Detect experience level from title and description"""
        title = job.get("job_title", "").lower()
        desc = job.get("job_description", "").lower()
        combined = title + " " + desc
        
        if any(word in combined for word in ["senior", "sr.", "lead", "principal", "staff"]):
            return "senior"
        elif any(word in combined for word in ["junior", "jr.", "entry", "graduate", "associate"]):
            return "entry"
        elif any(word in combined for word in ["intern", "internship", "co-op"]):
            return "internship"
        else:
            return "mid"
    
    def _parse_salary(self, job: dict) -> Optional[dict]:
        """Parse salary information"""
        min_salary = job.get("job_min_salary")
        max_salary = job.get("job_max_salary")
        
        if min_salary and max_salary:
            return {
                "min": int(min_salary),
                "max": int(max_salary),
                "currency": job.get("job_salary_currency", "USD"),
                "period": job.get("job_salary_period", "year")
            }
        return None
    
    def _parse_date(self, date_str: Optional[str]) -> str:
        """Parse date string"""
        if not date_str:
            return datetime.now().isoformat()
        
        try:
            # JSearch provides ISO format
            return date_str
        except:
            return datetime.now().isoformat()
    
    def _map_employment_type(self, emp_type: Optional[str]) -> str:
        """Map employment type"""
        if not emp_type:
            return "full_time"
        
        emp_type = emp_type.upper()
        mapping = {
            "FULLTIME": "full_time",
            "PARTTIME": "part_time",
            "CONTRACTOR": "contract",
            "INTERN": "internship"
        }
        return mapping.get(emp_type, "full_time")
    
    def _extract_requirements(self, highlights: dict) -> List[str]:
        """Extract requirements from job highlights"""
        qualifications = highlights.get("Qualifications", [])
        responsibilities = highlights.get("Responsibilities", [])
        return qualifications[:5]  # Top 5 requirements
    
    def _extract_benefits(self, highlights: dict) -> List[str]:
        """Extract benefits from job highlights"""
        benefits = highlights.get("Benefits", [])
        return benefits[:5]  # Top 5 benefits
    
    def _get_free_logo(self, company_name: str) -> Optional[str]:
        """Get company logo using free Clearbit"""
        if not company_name:
            return None
        
        name_lower = company_name.lower().strip()
        
        # Try known domains first
        for key, domain in self.known_domains.items():
            if key in name_lower:
                return f"https://logo.clearbit.com/{domain}"
        
        # Guess domain
        domain = self._guess_domain(company_name)
        return f"https://logo.clearbit.com/{domain}"
    
    def _guess_domain(self, company_name: str) -> str:
        """Guess company domain from name"""
        name = company_name.lower().strip()
        name = name.replace(" inc", "").replace(" llc", "")
        name = name.replace(" corporation", "").replace(" corp", "")
        name = name.replace(" limited", "").replace(" ltd", "")
        name = name.replace(" company", "").replace(" co", "")
        name = name.replace(",", "").replace(".", "")
        name = name.strip()
        
        domain = name.replace(" ", "").replace("-", "").replace("_", "")
        return f"{domain}.com"
