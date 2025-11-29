# PowerShell Workaround Instructions

## The Issue

PowerShell has trouble with the apostrophe in your OneDrive path:
```
C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\...
```

The apostrophe in `Nat'l` causes PowerShell parsing errors.

## Solution: Use CMD.exe Instead

### Option 1: Run Batch File Directly (Recommended)

1. **Open Command Prompt (cmd.exe)** - NOT PowerShell
   - Press `Win + R`
   - Type `cmd` and press Enter
   - OR search for "Command Prompt" in Start menu

2. **Navigate to the dashboard folder:**
   ```cmd
   cd /d "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis\10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"
   ```

3. **Run the batch file:**
   ```cmd
   install_and_deploy.bat
   ```

### Option 2: Double-Click the Batch File

1. Navigate to the folder in Windows Explorer
2. Double-click `install_and_deploy.bat`
3. This should open in cmd.exe automatically

### Option 3: Use the Wrapper Script

Double-click `run_with_cmd.bat` - this explicitly uses cmd.exe

## Why This Works

- **cmd.exe** handles apostrophes in paths correctly
- **PowerShell** interprets apostrophes as string delimiters
- Batch files (`.bat`) run in cmd.exe by default when double-clicked
- The issue only occurs when PowerShell wraps the command

## Alternative: Use Short Path (8.3 format)

If cmd.exe still has issues, you can use the short path format:

```cmd
cd /d C:\Users\edite\ONEDRI~1\Desktop\DREAMA~1\10_RED~1\redlining-dashboard
```

To find the short path, run:
```cmd
dir /x "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn"
```

## Quick Reference

**✅ DO THIS:**
- Use Command Prompt (cmd.exe)
- Double-click `.bat` files
- Use `cd /d` with quotes around paths

**❌ DON'T DO THIS:**
- Don't use PowerShell for these commands
- Don't run commands through Cursor's terminal (it uses PowerShell)

## If You Must Use PowerShell

If you need to use PowerShell, escape the apostrophe:

```powershell
cd "C:\Users\edite\OneDrive - Nat''l Community Reinvestment Coaltn\Desktop\DREAM Analysis\10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"
```

(Note: Two apostrophes `''` escape to one apostrophe in PowerShell)

