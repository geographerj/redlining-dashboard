@echo off
REM Check if C:\DREAM symbolic link exists and create it if needed
REM This is a workaround for PowerShell apostrophe issue in OneDrive path

echo ========================================
echo Checking C:\DREAM Symbolic Link
echo ========================================
echo.

if exist "C:\DREAM" (
    echo [OK] C:\DREAM symbolic link exists
    echo.
    echo Current link points to:
    dir C:\DREAM | findstr /C:"<SYMLINKD>"
    echo.
    echo You can use C:\DREAM path in scripts to avoid apostrophe issues.
) else (
    echo [INFO] C:\DREAM symbolic link does not exist
    echo.
    echo Would you like to create it? (Y/N)
    set /p CREATE_LINK=
    
    if /i "%CREATE_LINK%"=="Y" (
        echo.
        echo Creating symbolic link...
        echo This requires Administrator privileges.
        echo.
        mklink /D C:\DREAM "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis"
        
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo [SUCCESS] Symbolic link created!
            echo You can now use C:\DREAM in scripts to avoid apostrophe issues.
        ) else (
            echo.
            echo [ERROR] Failed to create symbolic link.
            echo Make sure you're running as Administrator.
            echo.
            echo You can create it manually by running this command as Administrator:
            echo mklink /D C:\DREAM "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis"
        )
    ) else (
        echo.
        echo Skipping symbolic link creation.
        echo Scripts will use full path (may have issues with PowerShell).
    )
)

echo.
pause

