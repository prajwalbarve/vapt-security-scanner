# VAPT Prospect Scraper - Setup & Usage Guide

## Overview
This script automatically searches for India-based startups with Web/API attack surfaces, applies your lead scoring criteria, and outputs daily qualified prospects ready for outreach.

**Features:**
- ✅ Searches multiple sources (Google, News, potential Crunchbase)
- ✅ Qualifies prospects by lead score (min 12, prioritize 15+)
- ✅ Detects buying signals (funding, hiring, launches, security focus)
- ✅ Deduplicates against historical tracker
- ✅ Ranks by relevance
- ✅ Outputs ready-to-use CSV for your outreach pipeline
- ✅ Persistent tracker maintains full history

---

## Installation

### 1. Install Python 3.8+
```bash
python3 --version  # Check if installed
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Free API Keys

#### Option A: SerpAPI (Google Search Results)
1. Go to https://serpapi.com/
2. Sign up for free account (100 free searches/month, ~$30-50/month for more)
3. Copy your API key from dashboard
4. Set environment variable:
   ```bash
   export SERPAPI_KEY="your_key_here"
   ```
   Or on Windows (PowerShell):
   ```powershell
   $env:SERPAPI_KEY="your_key_here"
   ```

#### Option B: NewsAPI (For Startup News)
1. Go to https://newsapi.org/
2. Register (free tier: 100 requests/day)
3. Copy API key
4. Set environment variable:
   ```bash
   export NEWS_API_KEY="your_key_here"
   ```

#### Option C: Free Alternative - Google Custom Search
- Google Custom Search offers 100 free searches/day
- Requires more setup but truly free
- Configure in script if using

### 4. Test the Script
```bash
python3 vapt_prospect_scraper.py
```

**Expected output:**
- Number of companies found
- Qualified prospects with scores 12+
- CSV export for spreadsheet import
- Tracker and leads file generated

---

## Daily Automation

### On macOS / Linux (Using Cron)

1. Make script executable:
   ```bash
   chmod +x vapt_prospect_scraper.py
   ```

2. Edit your crontab:
   ```bash
   crontab -e
   ```

3. Add one of these schedules:

   **Daily at 9 AM:**
   ```cron
   0 9 * * * cd /path/to/script && export SERPAPI_KEY="your_key" && export NEWS_API_KEY="your_key" && python3 vapt_prospect_scraper.py >> vapt_scraper.log 2>&1
   ```

   **Every weekday at 8 AM:**
   ```cron
   0 8 * * 1-5 cd /path/to/script && export SERPAPI_KEY="your_key" && python3 vapt_prospect_scraper.py >> vapt_scraper.log 2>&1
   ```

   **Every 6 hours:**
   ```cron
   0 */6 * * * cd /path/to/script && python3 vapt_prospect_scraper.py >> vapt_scraper.log 2>&1
   ```

4. Save and verify:
   ```bash
   crontab -l  # List active cron jobs
   ```

### On Windows (Using Task Scheduler)

1. Open Task Scheduler (search "Task Scheduler")
2. Click "Create Basic Task"
3. Name: "VAPT Daily Prospect Search"
4. Trigger: Daily, 9:00 AM
5. Action: Start a program
   - Program: `C:\Python39\python.exe` (your Python path)
   - Arguments: `C:\path\to\vapt_prospect_scraper.py`
   - Start in: `C:\path\to\script\directory`
6. Click OK

### Alternative: GitHub Actions (Cloud, Free)

If you push this to a GitHub repo:

1. Create `.github/workflows/vapt-daily.yml`:
   ```yaml
   name: VAPT Daily Prospect Search
   on:
     schedule:
       - cron: '0 9 * * *'  # Daily at 9 AM UTC
     workflow_dispatch:      # Manual trigger
   
   jobs:
     search:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - uses: actions/setup-python@v2
           with:
             python-version: '3.9'
         - run: pip install -r requirements.txt
         - run: python3 vapt_prospect_scraper.py
           env:
             SERPAPI_KEY: ${{ secrets.SERPAPI_KEY }}
             NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
         - uses: actions/upload-artifact@v2
           with:
             name: prospect-reports
             path: |
               vapt_leads_tracker.json
               vapt_qualified_leads.json
   ```

2. Add secrets to GitHub repo Settings > Secrets
3. Runs automatically on schedule or manually from Actions tab

---

## Output Files

### 1. `vapt_qualified_leads.json`
Full list of all qualified prospects (score 12+) discovered so far.

**Structure:**
```json
[
  {
    "name": "TechStartup India",
    "website": "https://techstartup.in",
    "description": "B2B SaaS platform for Indian enterprises",
    "domain": "techstartup.in",
    "lead_score": 16,
    "buying_signals": ["funding", "hiring"],
    "has_web_api": true,
    "is_b2b_saas": true,
    "is_technical": true,
    "source": "serpapi",
    "date_found": "2025-09-16T09:30:00"
  }
]
```

### 2. `vapt_leads_tracker.json`
Complete history of ALL researched companies (qualified and weak). Never overwrites—only adds.

**For each company:**
- Basic company info
- Lead score + qualification
- All detected signals
- Date discovered
- Research source

### 3. Console Output + CSV
When you run the script, it prints:
- Summary stats (total companies, new qualified today)
- Details of each new prospect
- CSV export (copy directly to spreadsheet)

**CSV format:**
```
Company Name,Website,Lead Score,Buying Signals,B2B SaaS,Technical,Web/API,Source
TechStartup India,https://techstartup.in,16,"funding;hiring",True,True,True,serpapi
```

---

## Integration with VAPT Outreach Pipeline

### Workflow:

1. **Script runs daily** → Outputs new qualified prospects
2. **You review CSV** → Companies ready for outreach
3. **Copy company details** → Into your main VAPT Lead Tracker (the artifact I'll build)
4. **Research decision-makers** → Verify contact info manually or with tools
5. **Draft personalized emails** → Using templates I'll provide
6. **Track delivery & replies** → In the VAPT tracker

---

## Customization

### Change Lead Score Weights
Edit `LEAD_SCORE_WEIGHTS` in the script:
```python
LEAD_SCORE_WEIGHTS = {
    "web_api_surface": 5,      # Most important
    "buying_signal": 4,
    "b2b_saas": 3,
    "technical_focus": 2,
    "company_size": 2,
}
```

### Add More Search Queries
Edit `SEARCH_QUERIES`:
```python
SEARCH_QUERIES = [
    "India B2B SaaS startup funded 2024 2025",
    "India API-first startup security",  # Add more queries
    "India startup founded 2024",
]
```

### Add More Buying Signals
Edit `BUYING_SIGNALS`:
```python
BUYING_SIGNALS = {
    "custom_signal": ["keyword1", "keyword2"],
}
```

### Increase Minimum Lead Score
```python
MIN_LEAD_SCORE = 15  # Instead of 12
```

---

## Troubleshooting

### No results found
- Check API keys are set correctly: `echo $SERPAPI_KEY`
- Test API directly: visit SerpAPI dashboard
- Check internet connection
- Try running with just one API source first

### "API key not set" warning
```bash
# Set keys properly before running:
export SERPAPI_KEY="your_actual_key"
export NEWS_API_KEY="your_actual_key"
python3 vapt_prospect_scraper.py
```

### Cron job not running
```bash
# Check cron logs:
log stream --predicate 'process == "cron"'  # macOS
sudo journalctl -u cron --follow            # Linux

# Test cron environment:
crontab -e  # Add this test line:
* * * * * env > /tmp/cron_env.txt
```

### Rate limits hit
- Free SerpAPI: 100/month (1-2 runs/day max)
- Free NewsAPI: 100/day
- Upgrade to paid plans or increase interval between runs
- Or use GitHub Actions (more free quota)

---

## Optimization Tips

### 1. Run frequency
- **Daily 9 AM**: Catches funding news, job postings
- **Twice weekly**: Reduces API costs, still finds new prospects
- **Weekly**: Low cost, slower discovery

### 2. Search queries
- Rotate keywords based on what's trending
- Focus on niches where you get best ROI (e.g., fintech, healthtech)

### 3. Lead score thresholds
- Start with 12+ to cast wider net
- After 30 days, increase to 15+ if getting low-quality leads
- Track which score thresholds convert best

### 4. API costs
- SerpAPI free: 100 searches/month ≈ $0 (limited)
- SerpAPI paid: $10-30/month for 1000+ searches
- NewsAPI free: 100/day ≈ $0
- **Total monthly cost: ~$0-50** for daily runs

---

## Next Steps

1. ✅ Install script and dependencies
2. ✅ Get API keys and set environment variables
3. ✅ Test script manually: `python3 vapt_prospect_scraper.py`
4. ✅ Set up daily automation (cron/Task Scheduler/GitHub Actions)
5. ✅ Review outputs daily or weekly
6. → I'll build the VAPT Lead Tracker artifact (intake new prospects, verify contacts, draft emails, track funnel)

---

## Questions?

Script location: `/home/claude/vapt_prospect_scraper.py`

Once you have this running daily, let me know and I'll build:
- **Interactive VAPT Lead Tracker** (persistent funnel)
- **Decision-maker research tools**
- **Email templates** (A/B variants)
- **Funnel analytics**
