@echo off
REM Workaround for PowerShell apostrophe path issue
REM This explicitly uses cmd.exe to avoid PowerShell parsing problems

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

REM Change to that directory
cd /d "%SCRIPT_DIR%"

REM Run the install and deploy script
call install_and_deploy.bat

