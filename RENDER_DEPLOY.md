# 🚀 Render.com Deployment Guide

## Step-by-Step Instructions

### Prerequisites
✅ GitHub account  
✅ Code uploaded to GitHub  

### Step 1: Sign Up on Render
1. Go to https://render.com
2. Click **"Get Started"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your repositories

### Step 2: Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Find `expense-tracker` repository
4. Click **"Connect"**

### Step 3: Configure Your Service

**Basic Settings:**
```
Name: expense-tracker
Region: Singapore (closest to Philippines)
Branch: main
Root Directory: (leave empty)
```

**Build Settings:**
```
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

**Instance Type:**
```
Choose: Free
```

### Step 4: Environment Variables (Optional but Recommended)

Click **"Advanced"** → **"Add Environment Variable"**

```
Key: SECRET_KEY
Value: your-random-secret-key-here-change-this
```

To generate a random secret key, use:
```python
import secrets
print(secrets.token_hex(32))
```

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. Watch the logs - should see "Build succeeded"
4. Status will change to **"Live"** ✅

### Step 6: Get Your Live URL

Your app will be available at:
```
https://expense-tracker.onrender.com
```

Or:
```
https://expense-tracker-yourname.onrender.com
```

### Step 7: Update README

Copy your live URL and update README.md:
```markdown
🌐 Live Demo: https://your-app.onrender.com
```

Then push to GitHub:
```bash
git add README.md
git commit -m "Added live demo link"
git push
```

## ⚠️ Important Notes

### Free Tier Limitations:
- ✅ **FREE forever**
- ⏱️ App sleeps after 15 min of inactivity
- 🐌 Takes 30-60 sec to wake up on first visit
- 💾 Database resets on each deploy (SQLite limitation)

### For Production (Upgrade Later):
- Use PostgreSQL instead of SQLite
- Paid tier ($7/month) - no sleep, faster, persistent database

## 🔧 Troubleshooting

### "Failed to build"
- Check requirements.txt has all packages
- Make sure Python version is correct in runtime.txt

### "Application failed to respond"
- Check Start Command: `gunicorn app:app`
- Make sure Procfile exists

### "Import errors"
- All dependencies in requirements.txt?
- Try: `pip freeze > requirements.txt` locally

### Database not persisting?
- SQLite resets on free tier
- Use PostgreSQL for persistent data (see Render docs)

## ✅ Success Checklist

- [ ] App builds successfully
- [ ] Status shows "Live"
- [ ] Can open the URL
- [ ] Can add expenses
- [ ] Dark mode works
- [ ] Charts display
- [ ] PDF export works

## 📱 Share Your Live Demo

Add to:
- ✅ Resume
- ✅ LinkedIn profile
- ✅ GitHub README
- ✅ Portfolio website

**Example:**
```
Expense Tracker - Live Demo
https://expense-tracker.onrender.com
```

---

🎉 Congratulations! Your app is now LIVE and accessible worldwide!
