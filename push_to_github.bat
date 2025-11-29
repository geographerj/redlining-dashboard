@echo off
echo ========================================
echo Pushing Redlining Dashboard to GitHub
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Initializing git...
git init

echo.
echo Step 2: Adding all files...
git add .

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit: Phase 1 React dashboard for Frost/Webster Bank redlining analysis"

echo.
echo Step 4: Adding remote repository...
git remote add origin https://github.com/geographerj/redlining-dashboard.git

echo.
echo Step 5: Setting main branch...
git branch -M main

echo.
echo Step 6: Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo Done! Check https://github.com/geographerj/redlining-dashboard
echo ========================================
pause

