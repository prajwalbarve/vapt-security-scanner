#!/usr/bin/env python3
"""
Simple Flask server to serve scraped leads as JSON API
Tracker fetches leads from this server automatically

Run this alongside your scraper:
    python3 lead_sync_server.py

Then tracker will auto-fetch from: http://localhost:5000/api/leads
"""

from flask import Flask, jsonify, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__)

# Path to scraped leads file (from scraper output)
LEADS_FILE = "vapt_qualified_leads.json"
TRACKER_FILE = "vapt_leads_tracker.json"

def load_leads():
    """Load leads from scraper output"""
    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def load_tracker():
    """Load full tracker data"""
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"leads": {}}
    return {"leads": {}}

@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Return all qualified leads as JSON"""
    leads = load_leads()
    
    # Convert to tracker format
    formatted = []
    for lead in leads:
        formatted.append({
            'id': abs(hash(lead.get('domain', lead.get('name')))) % (10 ** 8),
            'name': lead.get('name', ''),
            'website': lead.get('website', ''),
            'domain': lead.get('domain', ''),
            'score': lead.get('lead_score', 0),
            'signals': ','.join(lead.get('buying_signals', [])),
            'isBB2SaaS': lead.get('is_b2b_saas', False),
            'isTechnical': lead.get('is_technical', False),
            'hasWebAPI': lead.get('has_web_api', False),
            'source': lead.get('source', 'unknown'),
            'dateFound': lead.get('date_found', datetime.now().isoformat()),
            'status': 'qualified',
            'decisionMaker': '',
            'email': '',
            'replies': [],
            'sentiment': 'none',
            'initialSent': False,
            'followUp1': False,
            'followUp2': False,
            'notes': ''
        })
    
    return jsonify({
        'success': True,
        'count': len(formatted),
        'leads': formatted,
        'lastUpdated': os.path.getmtime(LEADS_FILE) if os.path.exists(LEADS_FILE) else None
    })

@app.route('/api/leads/new', methods=['GET'])
def get_new_leads():
    """Return only new leads (since last fetch)"""
    leads = load_leads()
    
    # Return last 10 (newest first)
    formatted = []
    for lead in leads[-10:]:
        formatted.append({
            'id': abs(hash(lead.get('domain', lead.get('name')))) % (10 ** 8),
            'name': lead.get('name', ''),
            'website': lead.get('website', ''),
            'domain': lead.get('domain', ''),
            'score': lead.get('lead_score', 0),
            'signals': ','.join(lead.get('buying_signals', [])),
        })
    
    return jsonify({
        'success': True,
        'count': len(formatted),
        'leads': formatted
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Health check - shows server status"""
    leads_count = len(load_leads())
    tracker_count = len(load_tracker().get('leads', {}))
    
    return jsonify({
        'success': True,
        'status': 'running',
        'scrapedLeads': leads_count,
        'trackerLeads': tracker_count,
        'server': 'VAPT Lead Sync Server',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def home():
    """Simple status page"""
    leads = load_leads()
    return f"""
    <h1>🎯 VAPT Lead Sync Server</h1>
    <p>Server is running!</p>
    <hr>
    <h2>📊 Status</h2>
    <ul>
        <li><strong>Scraped Leads:</strong> {len(leads)}</li>
        <li><strong>API Endpoint:</strong> <code>http://localhost:5000/api/leads</code></li>
        <li><strong>Status Check:</strong> <code>http://localhost:5000/api/status</code></li>
    </ul>
    <hr>
    <h2>📖 API Endpoints</h2>
    <ul>
        <li><code>GET /api/leads</code> - Get all scraped leads</li>
        <li><code>GET /api/leads/new</code> - Get newest leads</li>
        <li><code>GET /api/status</code> - Server status</li>
    </ul>
    <hr>
    <p>Tracker will auto-fetch from this server every 30 seconds.</p>
    """

if __name__ == '__main__':
    print("🚀 Starting VAPT Lead Sync Server...")
    print("📍 Running on http://localhost:5000")
    print("🔗 Tracker API: http://localhost:5000/api/leads")
    print("\nMake sure scraper is outputting leads to: vapt_qualified_leads.json")
    print("Tracker will auto-sync every 30 seconds.\n")
    
    app.run(debug=False, host='localhost', port=5000)
