@echo off
REM Workaround for PowerShell apostrophe issue in path
REM Uses C:\DREAM symbolic link to avoid apostrophe in OneDrive path

echo ========================================
echo Installing Dependencies and Deploying
echo ========================================
echo.

REM Try to use C:\DREAM symbolic link first (workaround for apostrophe issue)
if exist "C:\DREAM\10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard" (
    echo Using C:\DREAM symbolic link (workaround for apostrophe path issue)
    cd /d "C:\DREAM\10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"
) else (
    REM Fallback to script directory if symbolic link doesn't exist
    echo Using script directory (C:\DREAM symbolic link not found)
    cd /d "%~dp0"
)

echo Step 1: Installing npm dependencies...
echo (This may take a few minutes)
npm install

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: npm install failed!
    echo Make sure Node.js 14+ is installed.
    echo Check version with: node --version
    pause
    exit /b 1
)

echo.
echo Step 2: Building for production...
npm run build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo Step 3: Deploying to GitHub Pages...
npm run deploy

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Deployment failed!
    echo Make sure gh-pages is installed: npm install --save-dev gh-pages
    pause
    exit /b 1
)

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Go to: https://github.com/geographerj/redlining-dashboard/settings/pages
echo 2. Select "gh-pages" branch as source
echo 3. Save
echo.
echo Your dashboard will be at:
echo https://geographerj.github.io/redlining-dashboard/
echo.
pause

