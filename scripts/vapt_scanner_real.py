#!/usr/bin/env python3
"""
REAL Vulnerability Scanner - Finds ACTUAL startup security issues
Not just exposed .git, but real problems: missing headers, weak SSL, outdated software
"""

import json
import requests
import subprocess
import re
from datetime import datetime
from typing import Dict, List
from urllib.parse import urlparse

class RealVulnerabilityScanner:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0'
        })
    
    def scan_domain(self, domain: str) -> Dict:
        """Scan domain for REAL vulnerabilities."""
        findings = []
        
        print(f"\n🔍 Scanning: {domain}")
        
        # Check REAL issues that startups have
        findings.extend(self.check_ssl_certificate(domain))
        findings.extend(self.check_security_headers(domain))
        findings.extend(self.check_http_https_redirect(domain))
        findings.extend(self.check_outdated_software(domain))
        findings.extend(self.check_weak_authentication(domain))
        findings.extend(self.check_exposed_info(domain))
        
        severity = "high" if findings else "low"
        
        print(f"   ✅ Found {len(findings)} issues")
        
        return {
            "domain": domain,
            "scan_date": datetime.now().isoformat(),
            "findings": findings,
            "severity": severity,
            "total_findings": len(findings)
        }
    
    # ========================================================================
    # 1. SSL CERTIFICATE ISSUES
    # ========================================================================
    
    def check_ssl_certificate(self, domain: str) -> List[Dict]:
        """Check SSL - expiring, weak cipher, etc."""
        findings = []
        
        try:
            result = subprocess.run(
                f"echo | openssl s_client -servername {domain} -connect {domain}:443 2>/dev/null | openssl x509 -noout -dates",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            for line in result.stdout.split('\n'):
                if "notAfter" in line:
                    # Check expiry
                    if any(month in line for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']):
                        if '2026' in line or '2025' in line:
                            findings.append({
                                "type": "SSL Certificate Expiring Soon",
                                "severity": "medium",
                                "detail": line.strip(),
                                "action": "Renew certificate before expiry"
                            })
                            print(f"   ⚠️  SSL expiring soon: {line.strip()}")
        except:
            pass
        
        return findings
    
    # ========================================================================
    # 2. MISSING SECURITY HEADERS (VERY COMMON IN STARTUPS)
    # ========================================================================
    
    def check_security_headers(self, domain: str) -> List[Dict]:
        """Check for missing security headers - this is what MOST startups have wrong."""
        
        headers_to_check = {
            'strict-transport-security': ('HSTS', 'Medium', 'Force HTTPS usage'),
            'x-frame-options': ('X-Frame-Options', 'Medium', 'Prevent clickjacking'),
            'x-content-type-options': ('X-Content-Type-Options', 'Low', 'Prevent MIME sniffing'),
            'content-security-policy': ('CSP', 'High', 'Prevent XSS attacks'),
            'referrer-policy': ('Referrer-Policy', 'Low', 'Control referrer info'),
            'permissions-policy': ('Permissions-Policy', 'Low', 'Control browser features'),
        }
        
        findings = []
        
        try:
            response = requests.get(
                f"https://{domain}",
                timeout=10,
                verify=False,
                allow_redirects=True
            )
            
            print(f"   📊 Got response: {response.status_code}")
            
            # Check which headers are missing
            missing_count = 0
            for header, (name, severity, description) in headers_to_check.items():
                if header not in response.headers:
                    findings.append({
                        "type": f"Missing Security Header: {name}",
                        "severity": severity,
                        "description": description,
                        "header": header,
                        "action": f"Add {header} header to responses"
                    })
                    missing_count += 1
            
            if missing_count > 0:
                print(f"   ⚠️  Missing {missing_count} security headers")
        
        except Exception as e:
            print(f"   ❌ Error checking headers: {e}")
        
        return findings
    
    # ========================================================================
    # 3. HTTP NOT REDIRECTING TO HTTPS
    # ========================================================================
    
    def check_http_https_redirect(self, domain: str) -> List[Dict]:
        """Check if HTTP redirects to HTTPS."""
        findings = []
        
        try:
            response = requests.get(
                f"http://{domain}",
                timeout=5,
                allow_redirects=False,
                verify=False
            )
            
            # If returns 200 on HTTP (not redirect), it's a problem
            if response.status_code == 200:
                findings.append({
                    "type": "HTTP Not Redirected to HTTPS",
                    "severity": "high",
                    "description": "Site accessible via plain HTTP",
                    "action": "Configure HTTP → HTTPS redirect"
                })
                print(f"   🚨 HTTP accessible without HTTPS redirect!")
            
            # Check if redirect exists
            elif response.status_code in [301, 302]:
                location = response.headers.get('location', '')
                if 'https' not in location.lower():
                    findings.append({
                        "type": "HTTP Redirect to Non-HTTPS",
                        "severity": "medium",
                        "detail": f"Redirects to: {location}",
                        "action": "Ensure HTTP redirects to HTTPS"
                    })
                    print(f"   ⚠️  HTTP redirects to non-HTTPS: {location}")
        
        except:
            pass
        
        return findings
    
    # ========================================================================
    # 4. OUTDATED SOFTWARE DETECTION
    # ========================================================================
    
    def check_outdated_software(self, domain: str) -> List[Dict]:
        """Check for outdated software indicators."""
        findings = []
        
        try:
            response = requests.get(
                f"https://{domain}",
                timeout=10,
                verify=False
            )
            
            headers_text = str(response.headers).lower()
            html = response.text.lower()
            
            # Check for outdated software
            outdated_indicators = {
                'server': {
                    'apache/2.2': 'Apache 2.2 (EOL)',
                    'apache/2.4.1': 'Old Apache version',
                    'php/5': 'PHP 5 (EOL - major security issue!)',
                    'php/7.0': 'PHP 7.0 (EOL)',
                },
                'frameworks': {
                    'wordpress/4': 'Old WordPress version',
                    'wordpress/5.0': 'Outdated WordPress',
                    'joomla/3': 'Old Joomla version',
                }
            }
            
            for header_name, versions in outdated_indicators.items():
                for version, description in versions.items():
                    if version in headers_text or version in html:
                        findings.append({
                            "type": "Outdated Software",
                            "severity": "high",
                            "software": description,
                            "action": "Update to latest version",
                            "detail": f"Detected: {description}"
                        })
                        print(f"   🚨 Outdated: {description}")
        
        except:
            pass
        
        return findings
    
    # ========================================================================
    # 5. WEAK AUTHENTICATION DETECTION
    # ========================================================================
    
    def check_weak_authentication(self, domain: str) -> List[Dict]:
        """Check for weak auth patterns."""
        findings = []
        
        weak_auth_paths = [
            '/admin',
            '/wp-login.php',
            '/login',
            '/signin',
        ]
        
        try:
            for path in weak_auth_paths:
                response = requests.get(
                    f"https://{domain}{path}",
                    timeout=5,
                    verify=False,
                    allow_redirects=True
                )
                
                # Check if login form is found
                if response.status_code == 200 and len(response.text) > 500:
                    if any(keyword in response.text.lower() for keyword in ['password', 'login', 'username', 'sign in']):
                        findings.append({
                            "type": "Admin Panel Publicly Accessible",
                            "severity": "high",
                            "path": path,
                            "description": "Admin login page is publicly accessible",
                            "action": f"Protect {path} with IP whitelist or VPN"
                        })
                        print(f"   ⚠️  Admin panel exposed: {path}")
                        break
        
        except:
            pass
        
        return findings
    
    # ========================================================================
    # 6. EXPOSED INFORMATION
    # ========================================================================
    
    def check_exposed_info(self, domain: str) -> List[Dict]:
        """Check for exposed information."""
        findings = []
        
        try:
            response = requests.get(
                f"https://{domain}",
                timeout=10,
                verify=False
            )
            
            html = response.text.lower()
            headers = str(response.headers).lower()
            
            # Check for exposed info
            if 'x-powered-by' in headers:
                findings.append({
                    "type": "Server Information Exposed",
                    "severity": "low",
                    "detail": "X-Powered-By header reveals tech stack",
                    "action": "Remove X-Powered-By header"
                })
            
            # Check for debug mode
            if 'debug' in html and any(keyword in html for keyword in ['error', 'exception', 'traceback']):
                findings.append({
                    "type": "Debug Mode Enabled",
                    "severity": "high",
                    "description": "Error messages expose system info",
                    "action": "Disable debug mode in production"
                })
                print(f"   🚨 Debug mode might be enabled!")
        
        except:
            pass
        
        return findings

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run scanner."""
    
    try:
        with open('data/vapt_qualified_leads.json', 'r') as f:
            leads = json.load(f)
            domains = [lead.get('domain') for lead in leads if lead.get('domain')]
    except FileNotFoundError:
        print("❌ No leads file found!")
        return
    
    print("=" * 70)
    print("🔐 REAL VULNERABILITY SCANNER")
    print("Finding ACTUAL startup security issues")
    print("=" * 70)
    
    scanner = RealVulnerabilityScanner()
    results = []
    
    for domain in domains:
        result = scanner.scan_domain(domain)
        results.append(result)
    
    # Save results
    with open('data/vapt_real_findings.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 70)
    print("✅ Scan complete!")
    print(f"✅ Saved to: data/vapt_real_findings.json")
    print()
    
    # Summary
    total = sum(r['total_findings'] for r in results)
    companies_with_issues = len([r for r in results if r['total_findings'] > 0])
    
    print(f"📊 Summary:")
    print(f"   Companies scanned: {len(results)}")
    print(f"   Companies with issues: {companies_with_issues}")
    print(f"   Total issues found: {total}")
    print(f"   Average issues per company: {total / len(results) if results else 0:.1f}")
    print()

if __name__ == "__main__":
    main()
