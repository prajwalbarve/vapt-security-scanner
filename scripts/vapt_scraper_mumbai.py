#!/usr/bin/env python3
"""
Mumbai Startup Scraper - Finds REAL Mumbai-based startup websites
Targets: Tech, SaaS, FinTech, HealthTech startups based in Mumbai
"""

import json
import requests
import os
from datetime import datetime
from typing import List, Dict
from urllib.parse import urlparse

class MumbaiStartupScraper:
    
    def __init__(self):
        self.serpapi_key = os.environ.get('SERPAPI_KEY')
        self.scanned_domains = self.load_scanned_domains()
        print(f"📋 Already scanned: {len(self.scanned_domains)} domains")
    
    def load_scanned_domains(self) -> set:
        """Load already-scanned domains."""
        scanned = set()
        if os.path.exists('data/vapt_qualified_leads.json'):
            try:
                with open('data/vapt_qualified_leads.json', 'r') as f:
                    leads = json.load(f)
                    for lead in leads:
                        if 'domain' in lead:
                            scanned.add(lead['domain'].lower())
            except:
                pass
        return scanned
    
    def extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            domain = urlparse(url).netloc
            domain = domain.replace('www.', '').lower()
            return domain if domain else None
        except:
            return None
    
    def is_junk_source(self, domain: str, url: str) -> bool:
        """Filter out directories, news sites, etc."""
        junk_keywords = [
            # Directories
            'crunchbase', 'f6s', 'angel.co', 'producthunt', 'ycombinator',
            'wellfound', 'startupblink', 'tracxn', 'seedtable', 'topstartups',
            
            # News/Media
            'techcrunch', 'forbes', 'linkedin', 'medium', 'reddit',
            'youtube', 'twitter', 'facebook', 'instagram', 'quora',
            'wikipedia', 'entrepreneur.com', 'inc.com', 'bloomberg',
            'inc42', 'yourstory', 'thehindubusinessline', 'timesofindia',
            
            # Job boards
            'indeed', 'glassdoor', 'builtin',
            
            # Platforms
            'github', 'gitlab', 'google', 'amazon', 'aws', 'microsoft',
            'apple', 'slack', 'zoom', 'notion',
            
            # Generic
            'wikipedia', 'scribd', 'issuu',
        ]
        
        domain_lower = domain.lower()
        url_lower = url.lower()
        
        # Check domain
        for keyword in junk_keywords:
            if keyword in domain_lower:
                return True
        
        # Check if it's an article URL
        if any(path in url_lower for path in ['/article/', '/news/', '/blog/', '/post/', '/p/']):
            return True
        
        return False
    
    def search_mumbai_startups(self, query: str) -> List[str]:
        """Search for Mumbai startups."""
        
        if not self.serpapi_key:
            print(f"   ❌ SERPAPI_KEY not set!")
            return []
        
        try:
            print(f"\n🔍 Searching: {query}")
            
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "num": 10,
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
            print(f"   📊 Got {len(results)} results")
            
            domains = []
            
            for result in results:
                url = result.get('link', '')
                title = result.get('title', '')
                
                if not url:
                    continue
                
                domain = self.extract_domain(url)
                if not domain:
                    continue
                
                # Skip junk
                if self.is_junk_source(domain, url):
                    print(f"   ⏭️  Skip (junk): {domain}")
                    continue
                
                # Skip if already scanned
                if domain in self.scanned_domains:
                    print(f"   ⏭️  Already scanned: {domain}")
                    continue
                
                # Only .in and .com domains
                if not (domain.endswith('.in') or domain.endswith('.com')):
                    print(f"   ⏭️  Skip (not .in/.com): {domain}")
                    continue
                
                domains.append({
                    'domain': domain,
                    'title': title
                })
                print(f"   ✅ Found: {domain}")
            
            return domains
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
    
    def run(self):
        """Run scraper."""
        
        print("=" * 70)
        print("🏙️  MUMBAI STARTUP SCRAPER")
        print("Finding real Mumbai-based startups")
        print("=" * 70)
        
        clear = input("\n🗑️  Clear old data? (y/n): ").lower() == 'y'
        
        if clear:
            self.clear_old_data()
            self.scanned_domains = set()
        
        # MUMBAI-SPECIFIC search queries
        queries = [
            # Direct Mumbai startup searches
            "startup mumbai india",
            "tech startup mumbai",
            "saas startup mumbai",
            "fintech startup mumbai",
            "healthtech startup mumbai",
            "mumbai based startup",
            "startup company mumbai india",
            
            # Industry + location
            "app development company mumbai",
            "software startup india mumbai",
            "digital startup mumbai",
            
            # Growth + location
            "growing startup mumbai",
            "new startup mumbai",
            "startup ecosystem mumbai",
        ]
        
        all_results = []
        
        for query in queries:
            results = self.search_mumbai_startups(query)
            all_results.extend(results)
            self.scanned_domains.update([r['domain'] for r in results])
        
        # Remove duplicates
        seen = set()
        unique_results = []
        for result in all_results:
            if result['domain'] not in seen:
                seen.add(result['domain'])
                unique_results.append(result)
        
        print(f"\n✅ Found {len(unique_results)} new unique startup domains")
        
        if not unique_results:
            print("⚠️  No new startups found!")
            print("   Tip: Make sure SERPAPI_KEY is valid and has quota")
            return
        
        # Load existing leads
        existing_leads = []
        if os.path.exists('data/vapt_qualified_leads.json'):
            try:
                with open('data/vapt_qualified_leads.json', 'r') as f:
                    existing_leads = json.load(f)
            except:
                existing_leads = []
        
        # Create new companies
        new_companies = []
        for result in unique_results:
            new_companies.append({
                'name': result['title'].split(' - ')[0][:50] if result['title'] else result['domain'],
                'domain': result['domain'],
                'category': 'Startup',
                'location': 'Mumbai',
                'source': 'google_search_mumbai',
                'discovered_date': datetime.now().isoformat(),
                'buying_signal': False,
                'lead_score': 0
            })
        
        # Merge
        all_leads = new_companies + existing_leads
        
        # Save
        os.makedirs('data', exist_ok=True)
        with open('data/vapt_qualified_leads.json', 'w') as f:
            json.dump(all_leads, f, indent=2)
        
        print(f"✅ Total leads: {len(all_leads)}")
        print(f"✅ Saved to: data/vapt_qualified_leads.json")
        print()
        
        print("🏙️  Mumbai startups found:")
        for result in unique_results[:15]:
            print(f"   • {result['domain']}")
        
        if len(unique_results) > 15:
            print(f"   ... and {len(unique_results) - 15} more")
    
    def clear_old_data(self):
        """Archive old data."""
        files = [
            'data/vapt_qualified_leads.json',
            'data/vapt_real_findings.json',
            'data/vapt_strict_findings.json',
        ]
        
        for file in files:
            if os.path.exists(file):
                archive = file.replace('.json', f'_archive_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
                os.rename(file, archive)
                print(f"   📦 Archived: {archive}")
        
        print("✅ Old data cleared")

if __name__ == "__main__":
    scraper = MumbaiStartupScraper()
    scraper.run()
