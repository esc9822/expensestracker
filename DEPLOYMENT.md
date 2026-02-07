# Deployment Guide - Expense Tracker

## 🚀 How to Publish Your App

### **Option 1: Render.com (FREE & Easiest)**

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy to Render**
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name**: expense-tracker-yourname
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
   - Click "Create Web Service"
   - Your app will be live at: `https://expense-tracker-yourname.onrender.com`

### **Option 2: PythonAnywhere (FREE - Good for portfolios)**

1. **Sign up at https://www.pythonanywhere.com**
2. **Upload files**:
   - Go to "Files" tab
   - Upload all your project files
3. **Setup Web App**:
   - Go to "Web" tab → "Add a new web app"
   - Choose "Flask"
   - Python version: 3.10
   - Set path to your app.py
4. **Configure**:
   - Set working directory
   - Reload web app
   - Your app will be at: `https://yourusername.pythonanywhere.com`

### **Option 3: Railway.app (FREE tier available)**

1. **Install Railway CLI or use web**
2. **Deploy**:
   ```bash
   npm i -g @railway/cli
   railway login
   railway init
   railway up
   ```

### **Important: Change Secret Key for Production**

In `app.py`, change:
```python
app.secret_key = 'your-secret-key-change-in-production-12345'
```

To:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-me')
```

Then set environment variable `SECRET_KEY` in your hosting platform.

### **For Portfolio:**

Add these to your GitHub repo:
- ✅ `README.md` - Already created (PORTFOLIO_README.md)
- ✅ `requirements.txt` - Already created
- ✅ `.gitignore` - Excludes sensitive files
- ✅ Screenshots in `screenshots/` folder
- ✅ Live demo link in README

### **Demo Accounts (for Corporate Mode)**

If MODE = 'CORPORATE' in config.py:
- Admin: `admin` / `admin123`
- User: `user` / `user123`

### **Database Note:**

SQLite works for small projects but for production with multiple users, consider:
- PostgreSQL (Render provides free tier)
- MySQL

---

## 📝 Quick Checklist Before Publishing:

- [ ] Change secret key
- [ ] Test all features locally
- [ ] Add your name/info in footer
- [ ] Update README with live demo link
- [ ] Take screenshots for portfolio
- [ ] Test PDF export
- [ ] Test dark mode
- [ ] Verify all currencies work

## 🌐 Share Your Portfolio

Once deployed, add the link to:
- Your resume
- LinkedIn profile
- GitHub profile README
- Portfolio website

**Your live app URL will be**: `https://your-app-name.render.com` or similar
