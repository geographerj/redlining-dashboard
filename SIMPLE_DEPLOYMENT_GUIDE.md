# Simple Deployment Guide - Redlining Dashboard

## Goal
Get the dashboard online quickly so users can test it.

## Simplest Approach: Separate Repository + GitHub Pages

### Step 1: Create New GitHub Repository

1. Go to https://github.com/new
2. Repository name: `redlining-dashboard`
3. Owner: `geographerj` (or your account)
4. Visibility: **Public** (required for free GitHub Pages)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

### Step 2: Initialize Git in Dashboard Folder

Open PowerShell/Command Prompt and run:

```powershell
# Navigate to dashboard folder
cd "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis\10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Phase 1 React dashboard for Frost/Webster Bank redlining analysis"

# Add remote (replace YOUR_USERNAME if different)
git remote add origin https://github.com/geographerj/redlining-dashboard.git

# Push to main branch
git branch -M main
git push -u origin main
```

### Step 3: Generate Data Files (Once Excel is Available)

```powershell
# From DREAM Analysis root
cd "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis"

# Run data processing script (close Excel first!)
python "10_Redlining_Analysis_FL_Frost_Webster/process_existing_data.py"

# Copy generated files to dashboard
Copy-Item "10_Redlining_Analysis_FL_Frost_Webster\dashboard_data\*.json" -Destination "10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard\public\data\"
```

### Step 4: Install Dependencies & Test Locally

```powershell
cd "10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"

# Install dependencies (requires Node.js 14+)
npm install

# Start development server
npm start
```

This opens http://localhost:3000 - test it locally first!

### Step 5: Deploy to GitHub Pages

```powershell
# Build for production
npm run build

# Deploy to GitHub Pages
npm run deploy
```

### Step 6: Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/geographerj/redlining-dashboard`
2. Click **Settings** → **Pages**
3. Under "Source", select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
4. Click **Save**

### Step 7: Access Your Dashboard

Your dashboard will be live at:
```
https://geographerj.github.io/redlining-dashboard/
```

(May take 1-2 minutes to become available after deployment)

## Troubleshooting

### Node.js Version Issue
If `npm install` fails, you need Node.js 14 or higher:
- Check version: `node --version`
- Download from: https://nodejs.org/

### Data Files Missing
If dashboard shows "No data available":
- Make sure JSON files are in `public/data/` folder
- Check browser console for errors
- Verify file names match: `frost-bank-data.json`, `webster-bank-data.json`, `all-bank-data.json`

### GitHub Pages Not Working
- Wait 1-2 minutes after deployment
- Check repository Settings → Pages to verify `gh-pages` branch is selected
- Check Actions tab for deployment status

## Quick Commands Reference

```powershell
# Test locally
cd "10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"
npm start

# Deploy to GitHub Pages
npm run build
npm run deploy

# Update data and redeploy
python "10_Redlining_Analysis_FL_Frost_Webster/process_existing_data.py"
Copy-Item "10_Redlining_Analysis_FL_Frost_Webster\dashboard_data\*.json" -Destination "10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard\public\data\"
npm run build
npm run deploy
```

## Summary

1. ✅ Create new GitHub repo: `redlining-dashboard`
2. ✅ Initialize git and push code
3. ✅ Generate data files (when Excel available)
4. ✅ Test locally with `npm start`
5. ✅ Deploy with `npm run deploy`
6. ✅ Enable GitHub Pages in settings
7. ✅ Share URL: `https://geographerj.github.io/redlining-dashboard/`

**Total time**: ~15 minutes (once data files are ready)

