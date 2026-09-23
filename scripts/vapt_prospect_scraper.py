#!/usr/bin/env python3
"""
REAL VAPT Prospect Scraper - Actually calls APIs
Uses SerpAPI for Google Search results
"""

import json
import requests
import os
from datetime import datetime
from typing import List, Dict

# ============================================================================
# REAL SCRAPER - Calls SerpAPI
# ============================================================================

class RealProspectScraper:
    
    def __init__(self):
        self.serpapi_key = os.environ.get('SERPAPI_KEY')
        self.session = requests.Session()
        self.scanned_domains = self.load_scanned_domains()
        
        if not self.serpapi_key:
            print("⚠️  WARNING: SERPAPI_KEY not found in environment!")
            print("   Add to .env: SERPAPI_KEY=your_key_here")
        
        print(f"📋 Already scanned: {len(self.scanned_domains)} domains")
    
    def load_scanned_domains(self) -> set:
        """Load list of already-scanned domains."""
        scanned = set()
        
        # Check qualified leads
        if os.path.exists('data/vapt_qualified_leads.json'):
            try:
                with open('data/vapt_qualified_leads.json', 'r') as f:
                    leads = json.load(f)
                    for lead in leads:
                        if isinstance(lead, dict) and 'domain' in lead:
                            scanned.add(lead['domain'].lower())
            except:
                pass
        
        return scanned
    
    def is_new_domain(self, domain: str) -> bool:
        """Check if domain is NEW."""
        return domain.lower() not in self.scanned_domains
    
    def search_google(self, query: str) -> List[Dict]:
        """Search Google using SerpAPI."""
        
        if not self.serpapi_key:
            print(f"   ❌ SERPAPI_KEY not set! Can't search.")
            return []
        
        try:
            print(f"\n🔍 Searching: {query}")
            
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "num": 10,  # Get top 10 results
                "engine": "google"
            }
            
            response = requests.get(
                "https://serpapi.com/search",
                params=params,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"   ❌ API Error: {response.status_code}")
                return []
            
            data = response.json()
            
            if "error" in data:
                print(f"   ❌ API Error: {data['error']}")
                return []
            
            results = data.get("organic_results", [])
            print(f"   ✅ Found {len(results)} search results")
            
            return results
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
    
    def extract_domain_from_url(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            # Remove https://, http://, www.
            domain = url.replace("https://", "").replace("http://", "").replace("www.", "")
            # Get just the domain part (before path)
            domain = domain.split("/")[0]
            return domain.lower()
        except:
            return None
    
    def is_valid_startup_domain(self, url: str, title: str = "") -> bool:
        """Check if this is a real startup website (not a directory/news site)."""
        
        # REJECT these (not startup websites)
        junk_domains = {
            'indeed.com', 'linkedin.com', 'github.com', 'medium.com',
            'forbes.com', 'techcrunch.com', 'producthunt.com',
            'wikipedia.org', 'crunchbase.com', 'ycombinator.com',
            'facebook.com', 'twitter.com', 'youtube.com', 'reddit.com',
            'amazon.com', 'google.com', 'microsoft.com'
        }
        
        url_lower = url.lower()
        
        # Check if it's a junk domain
        for junk in junk_domains:
            if junk in url_lower:
                return False
        
        # Must be .in or .com
        if not ('.in' in url_lower or '.com' in url_lower):
            return False
        
        # Should NOT be a directory/news URL
        if any(x in url_lower for x in ['/lists/', '/top-', '/best-', '/news/', '/article/']):
            return False
        
        return True
    
    def run(self):
        """Run the scraper."""
        
        print("=" * 70)
        print("🔍 REAL PROSPECT SCRAPER - Using SerpAPI")
        print("=" * 70)
        
        # Ask to clear
        clear = input("\n🗑️  Clear old data before scanning? (y/n): ").lower() == 'y'
        
        if clear:
            self.clear_old_data()
            self.scanned_domains = set()
        
        # Search queries
        queries = [
            "best fintech startups india 2026",
            "top healthtech startups india 2026",
            "saas startups india 2026",
            "india edtech startups 2026",
            "logistics startups india 2026",
            "e-commerce startups india 2026",
            "ai startups india 2026",
        ]
        
        all_companies = []
        
        for query in queries:
            results = self.search_google(query)
            
            for result in results:
                url = result.get('link', '')
                title = result.get('title', '')
                
                if not url:
                    continue
                
                # Extract domain
                domain = self.extract_domain_from_url(url)
                if not domain:
                    continue
                
                # Check if valid startup
                if not self.is_valid_startup_domain(url, title):
                    print(f"   ⏭️  Skip (junk): {domain}")
                    continue
                
                # Check if NEW
                if not self.is_new_domain(domain):
                    print(f"   ⏭️  Skip (already scanned): {domain}")
                    continue
                
                # Add as new company
                company = {
                    'name': title.split(' - ')[0][:50],  # Use title as name
                    'domain': domain,
                    'category': 'Unknown',
                    'source': query,
                    'discovered_date': datetime.now().isoformat(),
                    'buying_signal': False,
                    'lead_score': 0
                }
                
                all_companies.append(company)
                self.scanned_domains.add(domain)
                print(f"   ✅ NEW: {domain}")
        
        print(f"\n✅ Found {len(all_companies)} NEW companies")
        
        if not all_companies:
            print("⚠️  No new companies found!")
            print("   Make sure:")
            print("   1. SERPAPI_KEY is set in .env")
            print("   2. You have API quota remaining")
            print("   3. Internet connection works")
            return
        
        # Load existing leads
        existing_leads = []
        if os.path.exists('data/vapt_qualified_leads.json'):
            try:
                with open('data/vapt_qualified_leads.json', 'r') as f:
                    existing_leads = json.load(f)
            except:
                existing_leads = []
        
        # Merge new + old
        all_leads = all_companies + existing_leads
        
        # Save
        os.makedirs('data', exist_ok=True)
        with open('data/vapt_qualified_leads.json', 'w') as f:
            json.dump(all_leads, f, indent=2)
        
        print(f"✅ Total leads (new + existing): {len(all_leads)}")
        print(f"✅ Saved to: data/vapt_qualified_leads.json")
        print()
        
        # Show sample
        print("📋 Sample companies found:")
        for company in all_companies[:5]:
            print(f"   • {company['domain']}")
    
    def clear_old_data(self):
        """Archive old data."""
        files = [
            'data/vapt_qualified_leads.json',
            'data/vapt_vulnerability_findings.json',
            'data/vapt_verified_findings.json',
        ]
        
        for file in files:
            if os.path.exists(file):
                archive = file.replace('.json', f'_archive_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
                os.rename(file, archive)
                print(f"   📦 Archived: {archive}")
        
        print("✅ Old data cleared")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    scraper = RealProspectScraper()
    scraper.run()
