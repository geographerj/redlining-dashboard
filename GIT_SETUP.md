# Git Setup Instructions for Redlining Dashboard

## Repository Information
- **Repository URL**: https://github.com/geographerj/NCRC-Big-Query-Access
- **Repository Name**: NCRC-Big-Query-Access
- **Owner**: geographerj

## Setup Steps

### Option 1: Add to Existing Repository (Recommended)

Since the redlining-dashboard is inside the `10_Redlining_Analysis_FL_Frost_Webster` folder, which is part of the DREAM Analysis project, you should add it to the existing repository.

#### From the DREAM Analysis root directory:

```bash
# Navigate to the root of DREAM Analysis
cd "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis"

# Check if this is already a git repository
git status

# If not initialized, initialize it
git init

# Add the remote (if not already added)
git remote add origin https://github.com/geographerj/NCRC-Big-Query-Access.git

# Or if remote already exists, verify it
git remote -v

# Stage the redlining-dashboard folder
git add "10_Redlining_Analysis_FL_Frost_Webster/redlining-dashboard/"

# Commit
git commit -m "Add redlining dashboard - Phase 1: Basic React dashboard for Frost/Webster Bank analysis"

# Push to repository
git push -u origin main
```

### Option 2: Standalone Repository (If you want separate repo)

If you want the redlining-dashboard to be in its own repository:

```bash
# Navigate to the dashboard folder
cd "10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Phase 1 React dashboard"

# Add remote (you'll need to create a new repo on GitHub first)
git remote add origin https://github.com/geographerj/redlining-dashboard.git

# Push
git push -u origin main
```

## Important Notes

1. **Check existing git status first**: The DREAM Analysis folder might already be a git repository. Check with `git status` from the root directory.

2. **GitHub Pages deployment**: For GitHub Pages to work, you'll need to:
   - Either create a separate repository for the dashboard
   - Or use a subfolder deployment strategy
   - Or deploy from a `gh-pages` branch

3. **Recommended approach**: Since the dashboard is part of the larger DREAM Analysis project, add it to the existing repository. The dashboard can be deployed separately using GitHub Actions or manually.

## Verify Setup

After setting up, verify with:

```bash
git remote -v
git status
git log --oneline -5
```

## Next Steps After Git Setup

1. Generate data files (once Excel is available):
   ```bash
   python "10_Redlining_Analysis_FL_Frost_Webster/process_existing_data.py"
   ```

2. Install dependencies:
   ```bash
   cd "10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"
   npm install
   ```

3. Test locally:
   ```bash
   npm start
   ```

4. Build and deploy:
   ```bash
   npm run build
   npm run deploy
   ```

