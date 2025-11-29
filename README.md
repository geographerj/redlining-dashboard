# Redlining Analysis Dashboard

Interactive dashboard for analyzing Frost Bank and Webster Bank lending patterns for potential redlining violations.

## Quick Start

### 1. Push Code to GitHub

The repository is ready at: https://github.com/geographerj/redlining-dashboard

**Option A: Use the batch script**
- Double-click `push_to_github.bat`

**Option B: Run manually in PowerShell**
```powershell
git init
git add .
git commit -m "Initial commit: Phase 1 React dashboard"
git remote add origin https://github.com/geographerj/redlining-dashboard.git
git branch -M main
git push -u origin main
```

### 2. Install Dependencies

```powershell
npm install
```

### 3. Generate Data Files (When Excel is Available)

```powershell
# From DREAM Analysis root
python "10_Redlining_Analysis_FL_Frost_Webster/process_existing_data.py"

# Copy JSON files to public/data/
Copy-Item "10_Redlining_Analysis_FL_Frost_Webster\dashboard_data\*.json" -Destination "10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard\public\data\"
```

### 4. Test Locally

```powershell
npm start
```

Opens at http://localhost:3000

### 5. Deploy to GitHub Pages

```powershell
npm run build
npm run deploy
```

Then in GitHub:
- Go to Settings → Pages
- Source: `gh-pages` branch
- Save

**Dashboard URL**: https://geographerj.github.io/redlining-dashboard/

## Features

- ✅ Lender selection (Frost Bank / Webster Bank)
- ✅ Hierarchical navigation (State → CBSA → County)
- ✅ Ratio-first approach with color coding
- ✅ Year filtering (2022, 2023, 2024)
- ✅ Sortable data tables
- ✅ NCRC brand colors

## Project Structure

```
redlining-dashboard/
├── public/
│   ├── data/          # JSON data files go here
│   └── index.html
├── src/
│   ├── components/   # React components
│   ├── context/      # Lender context
│   └── utils/        # Utilities and colors
└── package.json
```

## Next Steps

- [ ] Push code to GitHub
- [ ] Generate data files
- [ ] Test locally
- [ ] Deploy to GitHub Pages
- [ ] Share URL with users

## Documentation

- `SIMPLE_DEPLOYMENT_GUIDE.md` - Full deployment guide
- `PUSH_INSTRUCTIONS.md` - Git push instructions
- `DEPLOYMENT.md` - Detailed deployment info
