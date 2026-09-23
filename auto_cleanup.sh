#!/bin/bash

###############################################################################
# VAPT PROJECT AUTO-CLEANUP
# Run this ONE script and everything gets organized automatically
# Usage: bash auto_cleanup.sh
###############################################################################

set -e  # Exit on error

cd ~/Desktop/Project

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  VAPT PROJECT AUTO-CLEANUP                     ║"
echo "║          This will organize your messy project structure       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# ASK FOR CONFIRMATION
# ============================================================================

echo "⚠️  This will:"
echo "   1. Create proper directory structure"
echo "   2. Move scripts to scripts/"
echo "   3. Move data to data/"
echo "   4. Move docs to docs/"
echo "   5. DELETE exposed API key files (SECURITY!)"
echo "   6. Create .env and .gitignore files"
echo ""
read -p "Continue? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "🚀 Starting cleanup..."
echo ""

# ============================================================================
# 1. CREATE DIRECTORY STRUCTURE
# ============================================================================

echo "📁 Creating directories..."
mkdir -p scripts data docs logs output old_backups
echo "   ✅ Done"
echo ""

# ============================================================================
# 2. MOVE PYTHON SCRIPTS
# ============================================================================

echo "📜 Moving Python scripts to scripts/..."

if [ -f "vapt_prospect_scraper.py" ]; then
    mv vapt_prospect_scraper.py scripts/
    echo "   ✅ vapt_prospect_scraper.py"
fi

if [ -f "vapt_prospect_scraper_old.py" ]; then
    mv vapt_prospect_scraper_old.py old_backups/
    echo "   ✅ vapt_prospect_scraper_old.py → old_backups/"
fi

if [ -f "vapt_prospect_scraper_v2_strict.py" ]; then
    mv vapt_prospect_scraper_v2_strict.py old_backups/
    echo "   ✅ vapt_prospect_scraper_v2_strict.py → old_backups/"
fi

if [ -f "vapt_vulnerability_scanner_enhanced.py" ]; then
    mv vapt_vulnerability_scanner_enhanced.py old_backups/
    echo "   ✅ vapt_vulnerability_scanner_enhanced.py → old_backups/"
fi

if [ -f "vapt_vulnerability_verifier.py" ]; then
    mv vapt_vulnerability_verifier.py scripts/
    echo "   ✅ vapt_vulnerability_verifier.py"
fi

if [ -f "lead_sync_server.py" ]; then
    mv lead_sync_server.py scripts/
    echo "   ✅ lead_sync_server.py"
fi

echo ""

# ============================================================================
# 3. MOVE DATA FILES
# ============================================================================

echo "📊 Moving data files to data/..."

if [ -f "vapt_qualified_leads.json" ]; then
    mv vapt_qualified_leads.json data/
    echo "   ✅ vapt_qualified_leads.json"
fi

if [ -f "vapt_vulnerability_findings.json" ]; then
    mv vapt_vulnerability_findings.json data/
    echo "   ✅ vapt_vulnerability_findings.json"
fi

if [ -f "vapt_vulnerability_findings_enhanced.json" ]; then
    mv vapt_vulnerability_findings_enhanced.json data/
    echo "   ✅ vapt_vulnerability_findings_enhanced.json"
fi

if [ -f "vapt_verified_findings.json" ]; then
    mv vapt_verified_findings.json data/
    echo "   ✅ vapt_verified_findings.json"
fi

if [ -f "vapt_leads_tracker.json" ]; then
    mv vapt_leads_tracker.json data/
    echo "   ✅ vapt_leads_tracker.json"
fi

echo ""

# ============================================================================
# 4. MOVE DOCUMENTATION
# ============================================================================

echo "📖 Moving documentation to docs/..."

if [ -f "SETUP_GUIDE.md" ]; then
    mv SETUP_GUIDE.md docs/
    echo "   ✅ SETUP_GUIDE.md"
fi

if [ -f "QUICK_START.txt" ]; then
    mv QUICK_START.txt docs/
    echo "   ✅ QUICK_START.txt"
fi

if [ -f "SCRAPER_TO_TRACKER_SYNC.md" ]; then
    mv SCRAPER_TO_TRACKER_SYNC.md docs/
    echo "   ✅ SCRAPER_TO_TRACKER_SYNC.md"
fi

echo ""

# ============================================================================
# 5. DELETE EXPOSED API KEYS (SECURITY!)
# ============================================================================

echo "🔐 Removing exposed API keys..."

if [ -f "SERPAPI_KEY" ]; then
    rm SERPAPI_KEY
    echo "   ✅ Deleted SERPAPI_KEY (was exposed!)"
fi

if [ -f "NEWS_API_KEY" ]; then
    rm NEWS_API_KEY
    echo "   ✅ Deleted NEWS_API_KEY (was exposed!)"
fi

echo ""

# ============================================================================
# 6. DELETE TEMP FILES
# ============================================================================

echo "🗑️  Removing temporary files..."

if [ -f "'RUN '" ] || [ -f "RUN " ]; then
    rm -f 'RUN ' "RUN "
    echo "   ✅ Deleted 'RUN ' file"
fi

if [ -f "start_vapt_pipeline.sh" ]; then
    rm start_vapt_pipeline.sh
    echo "   ✅ Deleted start_vapt_pipeline.sh"
fi

echo ""

# ============================================================================
# 7. CREATE .env FILE
# ============================================================================

echo "⚙️  Creating .env file..."

if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# ============================================================================
# VAPT Project Environment Configuration
# KEEP THIS FILE SECRET - DO NOT COMMIT TO GIT
# ============================================================================

# API Keys
SERPAPI_KEY=your_serpapi_key_here
NEWS_API_KEY=your_news_api_key_here

# Flask Server
FLASK_HOST=localhost
FLASK_PORT=5000

# Database (optional)
DB_URL=sqlite:///vapt_tracker.db

# Email (for outreach automation - optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EOF
    chmod 600 .env
    echo "   ✅ Created .env"
    echo "   ⚠️  EDIT .env with your actual API keys!"
else
    echo "   ℹ️  .env already exists (skipped)"
fi

echo ""

# ============================================================================
# 8. CREATE .gitignore
# ============================================================================

echo "🔒 Creating .gitignore..."

if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# ============================================================================
# Git Ignore - Keep secrets and junk out of git
# ============================================================================

# Environment & Secrets
.env
.env.local
.env.*.local

# API Keys (in case they're stored as files)
SERPAPI_KEY
NEWS_API_KEY
*_key
*_secret

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
venv/
vapt_env/
env/
ENV/

# Virtual Environments
.venv
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Logs
*.log
logs/
*.log.*

# Data files (optional - uncomment if you don't want to track them)
# data/*.json
# output/

# Node (if using any Node tools)
node_modules/
package-lock.json

# Old backups
old_backups/
*_backup*/
*_archive_*

# Test artifacts
.pytest_cache/
.coverage
htmlcov/

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
EOF
    echo "   ✅ Created .gitignore"
else
    echo "   ℹ️  .gitignore already exists (skipped)"
fi

echo ""

# ============================================================================
# 9. SUMMARY
# ============================================================================

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   ✅ CLEANUP COMPLETE!                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "📁 NEW DIRECTORY STRUCTURE:"
echo ""
ls -la --group-directories-first 2>/dev/null | grep "^d" | awk '{print "   " $NF "/"}'
echo ""
ls -la --group-directories-first 2>/dev/null | grep "^-" | awk '{print "   " $NF}'
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🚀 NEXT STEPS:"
echo ""
echo "1️⃣  Edit .env with your API keys:"
echo "   nano .env"
echo ""
echo "2️⃣  Activate virtual environment:"
echo "   source vapt_env/bin/activate && source .env"
echo ""
echo "3️⃣  Copy fixed scripts (from outputs folder):"
echo "   cp /path/to/vapt_prospect_scraper_fixed.py scripts/"
echo "   cp /path/to/vapt_vulnerability_scanner_strict.py scripts/"
echo ""
echo "4️⃣  Run the fixed scraper:"
echo "   python3 scripts/vapt_prospect_scraper_fixed.py"
echo ""
echo "5️⃣  Run the fixed scanner:"
echo "   python3 scripts/vapt_vulnerability_scanner_strict.py"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "⚠️  IMPORTANT:"
echo "   • .env contains your API keys - KEEP IT SECRET"
echo "   • .gitignore prevents .env from being committed"
echo "   • Old scripts are in old_backups/ (safe to delete)"
echo "   • Never commit API keys to git"
echo ""

echo "✅ Your project is now clean and organized!"
echo ""
