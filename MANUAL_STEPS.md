# Manual Steps - Run These Yourself

Since terminal commands are timing out, here are the exact commands to run manually:

## Step 1: Install Dependencies

Open PowerShell or Command Prompt in the dashboard folder:

```powershell
cd "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis\10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"

npm install
```

**OR** double-click: `install_and_deploy.bat`

## Step 2: Build and Deploy

```powershell
npm run build
npm run deploy
```

**OR** the batch script does this automatically.

## Step 3: Enable GitHub Pages

1. Go to: https://github.com/geographerj/redlining-dashboard/settings/pages
2. Under "Source":
   - Branch: Select `gh-pages`
   - Folder: `/ (root)`
3. Click **Save**

## Step 4: Access Dashboard

Wait 1-2 minutes, then visit:
**https://geographerj.github.io/redlining-dashboard/**

## Troubleshooting

### "npm is not recognized"
- Install Node.js from https://nodejs.org/
- Restart your terminal after installing

### "npm install" fails
- Check Node version: `node --version` (needs 14+)
- Update Node.js if needed

### "gh-pages not found"
- Run: `npm install --save-dev gh-pages`
- Then try `npm run deploy` again

### Build errors
- Check for TypeScript errors
- Make sure all files are saved
- Try deleting `node_modules` and running `npm install` again

## Quick Reference

**All-in-one batch script**: Double-click `install_and_deploy.bat`

**Manual commands**:
```powershell
npm install
npm run build
npm run deploy
```

