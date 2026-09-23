# 🔄 Connect Scraper → Tracker (Auto-Sync Setup)

## What This Does

Your **Prospect Scraper** will now automatically feed leads into the **VAPT Lead Tracker** without any manual copying/pasting.

**Flow:**
```
Scraper (finds prospects) 
    ↓ saves to JSON
Sync Server (local API)
    ↓ serves as http://localhost:5000
Tracker (fetches every 30 sec)
    ↓ auto-imports new leads
Your dashboard (always up-to-date)
```

---

## 🚀 Setup (5 minutes)

### Step 1: Install Flask

```bash
pip install flask
```

Or if using virtual environment:
```bash
source vapt_env/bin/activate
pip install flask
```

### Step 2: Start the Sync Server

Open a **new terminal window** and run:

```bash
cd ~/Desktop/Project
python3 lead_sync_server.py
```

**You should see:**
```
🚀 Starting VAPT Lead Sync Server...
📍 Running on http://localhost:5000
🔗 Tracker API: http://localhost:5000/api/leads

Make sure scraper is outputting leads to: vapt_qualified_leads.json
Tracker will auto-sync every 30 seconds.
```

**Keep this terminal window open!** The server needs to run in the background.

### Step 3: Run Your Scraper (In Original Terminal)

```bash
cd ~/Desktop/Project
source vapt_env/bin/activate && source .env
python3 vapt_prospect_scraper.py
```

**Your scraper outputs to:** `vapt_qualified_leads.json`

### Step 4: Open the Tracker

Go to: https://claude.ai/artifact/L6baP7zYiJpoyH2597mwWQ

**You should see:**
- 🟢 Blue sync status bar at the top: "Auto-syncing with scraper..."
- 📍 "Sync Now" button (manual sync if needed)
- Auto-import happens every 30 seconds

---

## 📊 How It Works

### Scraper Runs:
```bash
python3 vapt_prospect_scraper.py
```
↓ Outputs to `vapt_qualified_leads.json`

### Sync Server (Always Running):
```bash
python3 lead_sync_server.py
```
↓ Serves JSON at `http://localhost:5000/api/leads`

### Tracker (Browser):
- Checks server every 30 seconds
- Auto-imports any new leads
- Shows sync status at top
- All data stored in browser (localStorage)

---

## 🔄 Complete Workflow (With Auto-Sync)

### Terminal 1: Sync Server
```bash
cd ~/Desktop/Project
python3 lead_sync_server.py
# Keep running in background
```

### Terminal 2: Scraper
```bash
cd ~/Desktop/Project
source vapt_env/bin/activate && source .env
python3 vapt_prospect_scraper.py
# Runs daily (same as before)
```

### Browser: Tracker
- Open: https://claude.ai/artifact/L6baP7zYiJpoyH2597mwWQ
- Keep open while scraper runs
- Auto-imports new leads every 30 seconds
- All data syncs automatically

---

## ⚙️ What Happens Automatically

1. **Scraper finds 5-10 new prospects** → Saves to `vapt_qualified_leads.json`
2. **Sync Server reads the file** → Serves as API
3. **Tracker fetches from API** → Auto-imports new leads
4. **You see them in tracker instantly** → No manual work!

**Example:**
- 9:00 AM: Scraper runs, finds 7 new companies
- 9:05 AM: Sync server has the data
- 9:06 AM: Tracker auto-syncs, shows 7 new leads
- You research, email, track results

---

## 📌 Sync Status Indicators

**Tracker shows:**

✅ **Blue bar + "Auto-syncing"** 
- Server is running and connected
- Auto-sync happening every 30 seconds

❌ **No blue bar**
- Server not running
- Start with: `python3 lead_sync_server.py`

---

## 🎯 Manual Sync

If you want to force a sync immediately:
- Click **"⟳ Sync Now"** button in tracker
- Fetches latest leads from server
- Imports any new ones

---

## 📁 Files You Need

All included in `/mnt/user-data/outputs/`:

1. **vapt_prospect_scraper.py** - Your prospect finder
2. **lead_sync_server.py** - New! Syncs scraper to tracker
3. **vapt_tracker_v2.html** - Updated tracker with auto-sync
4. **.env** - Your API keys

---

## 🛠️ Troubleshooting

### "Sync server not running" message?
```bash
# Make sure server is started
python3 lead_sync_server.py

# Should say: "Running on http://localhost:5000"
```

### "Sync Status doesn't appear"?
- Wait 30 seconds (first sync check happens after 30 sec)
- Or click "Sync Now" button
- Or refresh tracker page

### "Leads not showing up"?
- Check tracker shows in "Leads" tab
- Refresh page (Ctrl+R)
- Check browser console for errors (F12)

### "Port already in use"?
```bash
# If port 5000 is busy, modify lead_sync_server.py:
# Change: app.run(..., port=5000)
# To:     app.run(..., port=5001)
```

---

## 🚀 Daily Routine (After Setup)

### Morning:
```bash
# Terminal 1: Start sync server (ONE TIME)
python3 lead_sync_server.py

# Terminal 2: Run scraper daily
python3 vapt_prospect_scraper.py
```

### Browser:
```
Open tracker → Watch leads auto-populate
Research → Send emails → Track replies
(All automatic sync in background)
```

### That's it!

---

## 📊 API Endpoints (If You Need Them)

The sync server provides these endpoints:

**Get all leads:**
```
GET http://localhost:5000/api/leads
```

**Get server status:**
```
GET http://localhost:5000/api/status
```

**Example response:**
```json
{
  "success": true,
  "count": 42,
  "leads": [
    {
      "name": "Decentro",
      "website": "https://decentro.tech",
      "score": 14,
      "signals": "funding"
    }
  ]
}
```

---

## ✅ You're Done!

You now have a **fully automated prospect pipeline**:

1. ✅ **Scraper** finds prospects daily
2. ✅ **Sync Server** connects scraper to tracker
3. ✅ **Tracker** auto-imports leads every 30 seconds
4. ✅ **You** research, email, track, close deals

**No manual CSV copying anymore!** 🎉

---

## 🎯 Next Steps

1. Install Flask: `pip install flask`
2. Start sync server: `python3 lead_sync_server.py`
3. Run scraper: `python3 vapt_prospect_scraper.py`
4. Open tracker: https://claude.ai/artifact/L6baP7zYiJpoyH2597mwWQ
5. Watch leads auto-populate! 🚀

Let me know if you need any help! 🎯
