# NET_SCAN - Virtual Environment Setup Guide

This guide covers setting up NET_SCAN using Python virtual environments for both Windows and Linux systems.

## Why Use Virtual Environments?

Virtual environments provide:
- **Isolation**: Each project has its own Python packages
- **Dependency Management**: Prevents conflicts between projects
- **Reproducibility**: Same setup works across different machines
- **Fixes pip Issues**: Resolves most "command not found" errors
- **Clean Uninstall**: Simply delete the venv folder to remove everything

## Quick Setup

### Windows (PowerShell)

```powershell
# 1. Navigate to project
cd net-scan

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
.\\venv\\Scripts\\Activate.ps1

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt
python -m playwright install
pip install -e .

# 6. Verify
net-scan --version
```

### Linux/macOS (Bash/Zsh)

```bash
# 1. Navigate to project
cd net-scan

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Upgrade pip
python3 -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt
python -m playwright install
pip install -e .

# 6. Verify
net-scan --version
```

---

## Detailed Windows Setup

### Step 1: Check Python Installation

```powershell
python --version
```

**Expected output:** `Python 3.11.0` or higher

If not found, [download Python](https://www.python.org/downloads/) and ensure "Add Python to PATH" is checked during installation.

### Step 2: Open Project Folder

```powershell
cd "C:\Path\To\net-scan"
```

Or in PowerShell:
```powershell
Set-Location "C:\Path\To\net-scan"
```

### Step 3: Create Virtual Environment

```powershell
python -m venv venv
```

This creates a `venv` folder containing Python interpreter and package manager.

### Step 4: Activate Virtual Environment

```powershell
.\\venv\\Scripts\\Activate.ps1
```

**You should see:** `(venv)` at the beginning of your terminal prompt

**If you get an error:**
```powershell
# Allow script execution (one-time setup)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then retry activation
.\\venv\\Scripts\\Activate.ps1
```

### Step 5: Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### Step 6: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 7: Install Playwright Browsers

```powershell
python -m playwright install
```

This downloads browser binaries required for JavaScript rendering. Takes ~500MB disk space.

### Step 8: Install NET_SCAN

```powershell
pip install -e .
```

The `-e` flag installs in "editable" mode, allowing you to modify code and test immediately.

### Step 9: Verify Installation

```powershell
net-scan --version
net-scan config
```

### Step 10: Deactivate When Done

```powershell
deactivate
```

---

## Detailed Linux/macOS Setup

### Step 1: Check Python Installation

```bash
python3 --version
```

**Expected output:** `Python 3.11` or higher

If not found:
- **Ubuntu/Debian:** `sudo apt-get install python3 python3-venv`
- **macOS:** `brew install python3` (if Homebrew installed) or [download](https://www.python.org/downloads/)

### Step 2: Open Project Folder

```bash
cd ~/path/to/net-scan
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
```

This creates a `venv` folder containing Python interpreter and package manager.

### Step 4: Activate Virtual Environment

```bash
source venv/bin/activate
```

**You should see:** `(venv)` at the beginning of your terminal prompt

### Step 5: Upgrade pip

```bash
python3 -m pip install --upgrade pip
```

### Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 7: Install Playwright Browsers

```bash
python -m playwright install
```

This downloads browser binaries required for JavaScript rendering. Takes ~500MB disk space.

### Step 8: Install NET_SCAN

```bash
pip install -e .
```

The `-e` flag installs in "editable" mode, allowing you to modify code and test immediately.

### Step 9: Verify Installation

```bash
net-scan --version
net-scan config
```

### Step 10: Deactivate When Done

```bash
deactivate
```

---

## Troubleshooting

### Problem: "python: command not found" (Linux/macOS)

**Solution:**
```bash
# Use python3 instead
python3 -m venv venv
```

### Problem: "venv activation fails" (Windows)

**Error:** `cannot be loaded because running scripts is disabled on this system`

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then retry activation.

### Problem: "pip: command not found"

**Solution:** Use the module syntax instead:
```bash
# Instead of: pip install
# Use:
python -m pip install          # Windows
python3 -m pip install         # Linux/macOS
```

### Problem: "net-scan: command not found"

**Causes:**
1. Virtual environment not activated
2. NET_SCAN not installed with `pip install -e .`

**Solution:**
```bash
# Verify venv is activated (should see (venv) in prompt)
# If not, activate it:
.\\venv\\Scripts\\Activate.ps1    # Windows
source venv/bin/activate          # Linux/macOS

# Reinstall NET_SCAN
pip install -e .
```

### Problem: "Module not found: playwright"

**Solution:** Playwright not fully installed

```bash
python -m playwright install
```

### Problem: Slow installation (pip seems stuck)

**Solution:** Increase timeout

```bash
pip install --default-timeout=1000 -r requirements.txt
```

### Problem: "Permission denied" (Linux/macOS)

**Solution:** You likely used `sudo`. Don't use sudo with venv. Delete venv and recreate:

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Managing Virtual Environments

### List all packages in venv

```bash
pip list
```

### Export installed packages

```bash
pip freeze > requirements-export.txt
```

### Install additional packages

```bash
pip install package_name
```

### Uninstall packages

```bash
pip uninstall package_name
```

### Completely remove venv

```powershell
# Windows
Remove-Item -Recurse venv

# Linux/macOS
rm -rf venv
```

Then recreate with `python -m venv venv` (Windows) or `python3 -m venv venv` (Linux/macOS)

---

## Using NET_SCAN in Virtual Environment

Always ensure venv is activated before running NET_SCAN:

### Windows
```powershell
.\\venv\\Scripts\\Activate.ps1
net-scan scan https://target.com
```

### Linux/macOS
```bash
source venv/bin/activate
net-scan scan https://target.com
```

---

## Advanced: Creating Portable venv Script

### Windows (create `setup.bat`)

```batch
@echo off
python -m venv venv
call venv\\Scripts\\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install
pip install -e .
echo Setup complete!
```

Run with: `setup.bat`

### Linux/macOS (create `setup.sh`)

```bash
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install
pip install -e .
echo "Setup complete!"
```

Run with:
```bash
chmod +x setup.sh
./setup.sh
```

---

## Python Version Management

### Windows: Multiple Python Versions

If you have multiple Python versions installed:

```powershell
# Use Python 3.11 specifically
py -3.11 -m venv venv
```

### Linux/macOS: Multiple Python Versions

```bash
# Use Python 3.11 specifically
python3.11 -m venv venv
```

---

## System-Wide pip (Not Recommended)

If you absolutely cannot use virtual environments:

```bash
# Windows
python -m pip install --upgrade pip
pip install -r requirements.txt

# Linux/macOS
python3 -m pip install --user -r requirements.txt
```

⚠️ **Warning:** This can conflict with other Python projects and system packages. Virtual environments are strongly recommended.

---

## Questions?

Refer to the [QUICKSTART.md](QUICKSTART.md) for basic usage or [README.md](README.md) for full documentation.
