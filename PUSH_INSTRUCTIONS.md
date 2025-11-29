# Push Code to GitHub - Instructions

## Repository Ready ✅
**URL**: https://github.com/geographerj/redlining-dashboard

## Quick Push (Windows)

### Option 1: Use the Batch Script
Double-click: `push_to_github.bat`

### Option 2: Manual Commands

Open PowerShell in the dashboard folder and run:

```powershell
cd "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis\10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create commit
git commit -m "Initial commit: Phase 1 React dashboard for Frost/Webster Bank redlining analysis"

# Add remote
git remote add origin https://github.com/geographerj/redlining-dashboard.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

## After Pushing

1. **Verify on GitHub**: Check https://github.com/geographerj/redlining-dashboard
2. **Install dependencies**: `npm install`
3. **Deploy to GitHub Pages**: `npm run build && npm run deploy`
4. **Enable Pages**: Settings → Pages → Select `gh-pages` branch

## Troubleshooting

### "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/geographerj/redlining-dashboard.git
```

### Authentication Required
- GitHub may prompt for credentials
- Use Personal Access Token if 2FA is enabled
- Or use GitHub Desktop for easier authentication

