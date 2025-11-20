#!/usr/bin/env python3
"""
Test script for LinkedIn jobs API
Run this to verify your setup works!
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.simple_job_service import SimpleJobService

def test_job_service():
    """Test the job service"""
    print("🧪 Testing LinkedIn Jobs API...")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        print("❌ ERROR: RAPIDAPI_KEY not found in .env file")
        print("   Please add your RapidAPI key to .env")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    print()
    
    # Initialize service
    try:
        service = SimpleJobService()
        print("✅ Service initialized successfully")
    except Exception as e:
        print(f"❌ ERROR initializing service: {e}")
        return False
    
    print()
    
    # Test job search
    print("🔍 Searching for 'iOS Developer' jobs...")
    print()
    
    try:
        jobs = service.search_jobs(
            keywords="iOS Developer",
            location="San Francisco",
            limit=5
        )
        
        if not jobs:
            print("⚠️  No jobs found. This might be normal if:")
            print("   - LinkedIn API is rate limited")
            print("   - No jobs match the criteria")
            print("   - API key needs verification")
            return False
        
        print(f"✅ Found {len(jobs)} jobs!")
        print()
        print("📋 Sample Jobs:")
        print("=" * 50)
        
        for i, job in enumerate(jobs[:3], 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']} ({job['location_type']})")
            if job['salary']:
                print(f"   Salary: ${job['salary']['min']:,} - ${job['salary']['max']:,}")
            if job['company_logo']:
                print(f"   Logo: {job['company_logo']}")
            print(f"   URL: {job['application_url'][:60]}...")
        
        print()
        print("=" * 50)
        print("🎉 SUCCESS! LinkedIn jobs API is working!")
        print()
        print("Next steps:")
        print("1. Start the backend: uvicorn main:app --reload")
        print("2. Test in browser: http://localhost:8000/api/docs")
        print("3. Run iOS app and check Jobs tab")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR searching jobs: {e}")
        print()
        print("Possible issues:")
        print("- Check your RapidAPI key is correct")
        print("- Verify you're subscribed to LinkedIn Data API on RapidAPI")
        print("- Check your internet connection")
        return False

if __name__ == "__main__":
    success = test_job_service()
    sys.exit(0 if success else 1)
