# C:\DREAM Symbolic Link Workaround

## Overview

The project uses a symbolic link at `C:\DREAM` to avoid PowerShell parsing issues with the apostrophe in the OneDrive path:

```
C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis
```

## How It Works

The symbolic link creates an alias without apostrophes:
- **Full path**: `C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis`
- **Symbolic link**: `C:\DREAM`
- **Both point to the same location**

## Creating the Symbolic Link

### Option 1: Use the Check Script

Run `check_dream_link.bat` - it will check if the link exists and offer to create it.

### Option 2: Manual Creation (Requires Admin)

Open Command Prompt **as Administrator** and run:

```cmd
mklink /D C:\DREAM "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis"
```

**Note**: The `/D` flag creates a directory symbolic link (not a file link).

### Option 3: PowerShell (Requires Admin)

```powershell
New-Item -ItemType SymbolicLink -Path "C:\DREAM" -Target "C:\Users\edite\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\DREAM Analysis"
```

## Using the Symbolic Link

### In Batch Files

```batch
REM Use C:\DREAM instead of full path
cd /d "C:\DREAM\10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard"
```

### In Python Scripts

```python
from pathlib import Path

# Use C:\DREAM instead of full path
dream_root = Path(r"C:\DREAM")
script_path = dream_root / "10_Redlining_Analysis_FL_Frost_Webster" / "redlining-dashboard"
```

### In Command Line

```cmd
cd C:\DREAM\10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard
npm install
```

## Benefits

✅ **No apostrophe issues** - PowerShell can parse `C:\DREAM` correctly  
✅ **Shorter paths** - Easier to type and read  
✅ **Consistent** - Same path works in cmd.exe, PowerShell, and Python  
✅ **Already in use** - Many existing scripts use this pattern

## Verification

Check if the link exists:
```cmd
dir C:\DREAM
```

You should see the contents of your DREAM Analysis folder.

Check what it points to:
```cmd
dir C:\DREAM | findstr /C:"<SYMLINKD>"
```

## Files Using This Pattern

- `run_test_via_dream.py` - Uses `C:\dream` (lowercase)
- `run_schema_with_dream_link.py` - Uses `C:\DREAM` (uppercase)
- `launch_api_test.py` - Checks for `C:\DREAM` first
- Many other scripts in the project

## Troubleshooting

### "Cannot create a file when that file already exists"
- The symbolic link already exists
- Delete it first: `rmdir C:\DREAM` (if it's a directory link)
- Or verify it points to the correct location

### "You do not have sufficient privilege"
- Run Command Prompt as Administrator
- Right-click → "Run as administrator"

### Link points to wrong location
- Delete the existing link: `rmdir C:\DREAM`
- Recreate it with the correct path

## Updated Batch Files

The `install_and_deploy.bat` script now:
1. Checks if `C:\DREAM` exists
2. Uses `C:\DREAM\10_Redlining_Analysis_FL_Frost_Webster\redlining-dashboard` if available
3. Falls back to script directory if link doesn't exist

This ensures compatibility whether the symbolic link exists or not.

