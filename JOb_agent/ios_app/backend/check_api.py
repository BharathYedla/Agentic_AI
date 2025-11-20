#!/usr/bin/env python3
"""
Diagnostic script for RapidAPI LinkedIn Jobs
Helps identify subscription and API issues
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_rapidapi_subscription():
    """Check RapidAPI subscription status"""
    print("🔍 RapidAPI LinkedIn Jobs - Diagnostic Tool")
    print("=" * 60)
    print()
    
    # Get API key
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        print("❌ ERROR: RAPIDAPI_KEY not found in .env")
        return False
    
    print(f"✅ API Key found: {api_key[:15]}...")
    print()
    
    # Test different endpoints
    endpoints = [
        {
            "name": "LinkedIn Data API (search-jobs)",
            "url": "https://linkedin-data-api.p.rapidapi.com/search-jobs",
            "params": {"keywords": "developer", "locationId": "0"},
            "host": "linkedin-data-api.p.rapidapi.com"
        },
        {
            "name": "LinkedIn Jobs Search API",
            "url": "https://linkedin-jobs-search.p.rapidapi.com/",
            "params": {"keywords": "developer"},
            "host": "linkedin-jobs-search.p.rapidapi.com"
        },
        {
            "name": "JSearch (Alternative)",
            "url": "https://jsearch.p.rapidapi.com/search",
            "params": {"query": "iOS developer", "num_pages": "1"},
            "host": "jsearch.p.rapidapi.com"
        }
    ]
    
    print("Testing available APIs...")
    print()
    
    working_apis = []
    
    for endpoint in endpoints:
        print(f"📡 Testing: {endpoint['name']}")
        print(f"   URL: {endpoint['url']}")
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": endpoint['host']
        }
        
        try:
            response = requests.get(
                endpoint['url'],
                headers=headers,
                params=endpoint['params'],
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS! This API works!")
                data = response.json()
                
                # Try to get job count
                if 'data' in data:
                    print(f"   📊 Found {len(data.get('data', []))} jobs")
                elif 'jobs' in data:
                    print(f"   📊 Found {len(data.get('jobs', []))} jobs")
                
                working_apis.append(endpoint)
                print()
                
            elif response.status_code == 403:
                print(f"   ⚠️  403 Forbidden - Not subscribed to this API")
                print(f"   💡 Subscribe at: https://rapidapi.com/")
                print()
                
            elif response.status_code == 429:
                print(f"   ⚠️  429 Rate Limited - Too many requests")
                print()
                
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:100]}")
                print()
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    print("=" * 60)
    print()
    
    if working_apis:
        print(f"🎉 SUCCESS! Found {len(working_apis)} working API(s):")
        print()
        for api in working_apis:
            print(f"   ✅ {api['name']}")
        print()
        print("📝 Next steps:")
        print("   1. Update simple_job_service.py to use working API")
        print("   2. Start backend: uvicorn main:app --reload")
        print("   3. Test in iOS app")
        return True
    else:
        print("❌ No working APIs found!")
        print()
        print("📝 Action required:")
        print()
        print("1. Go to https://rapidapi.com/")
        print("2. Sign in with your account")
        print("3. Subscribe to one of these APIs (all have free tiers):")
        print()
        print("   Option 1: JSearch (Recommended)")
        print("   https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch")
        print("   Free: 150 requests/month")
        print()
        print("   Option 2: LinkedIn Jobs Search")
        print("   https://rapidapi.com/rockapis-rockapis-default/api/linkedin-jobs-search")
        print("   Free: 100 requests/month")
        print()
        print("   Option 3: LinkedIn Data API")
        print("   https://rapidapi.com/rockapis-rockapis-default/api/linkedin-data-api")
        print("   Free: 100 requests/month")
        print()
        print("4. After subscribing, run this script again")
        return False

if __name__ == "__main__":
    import sys
    success = check_rapidapi_subscription()
    sys.exit(0 if success else 1)
